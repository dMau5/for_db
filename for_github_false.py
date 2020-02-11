from pickle import load, dump
from pony.orm import db_session
from multiprocessing import Process, Queue
from CGRdb import Molecule, load_schema
from itertools import islice, cycle, filterfalse

load_schema('name', user='postgres', password='pass', host='host', database='postgres')


with open('pairs_from_reactant_to_product.pickle', 'rb') as f:
    pairs = load(f)

with open('fingerprints.pickle', 'rb') as f0:
    fps = load(f0)

with open('list_of_A.pickle', 'rb') as f1:
    sigma = load(f1)

with open('similarities_array.pickle', 'rb') as f2:
    big = load(f2)

with open('old_to_new.pickle', 'rb') as f3:
    old_to_new = load(f3)

with open('new_to_old.pickle', 'rb') as f4:
    new_to_old = load(f4)


def evaluation(query, res):
    """
    оценка нод.
    возвращает танимото для пары запрос-результат.
    """
    qc, rc, common = len(query), len(res), len(query.intersection(res))
    return common / (qc + rc - common)


def roundrobin1(*iterables):
    num_active = len(iterables)
    iterables = cycle(iterables)
    while num_active:
        try:
            for nxt in iterables:
                yield next(nxt)
        except StopIteration:
            num_active -= 1
            iterables = cycle(islice(iterables, num_active))


def roundrobin2(iterables):
    dt = []
    for tu_sh, tu, A_sh in iterables:
        try:
            yield next(tu_sh), tu, A_sh
            dt.append((tu_sh, tu, A_sh))
        except StopIteration:
            pass

    num_active = len(dt)
    iterables = cycle(dt)
    while num_active:
        try:
            for tu_sh, tu, A_sh in iterables:
                yield next(tu_sh), tu, A_sh
        except StopIteration:
            num_active -= 1
            iterables = cycle(islice(iterables, num_active))


def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def worker(p, o):
    for m_A, m_A_sh, t_u_sh in iter(p.get, 'STOP'):
        fp_1 = fps[t_u_sh]
        t_unics = set(pairs[m_A]) - set(pairs[m_A_sh])
        index = 0
        for t_u in t_unics:
            fp_2 = fps[t_u]
            new_ind = evaluation(fp_1, fp_2)
            if new_ind > index:
                index = new_ind
        with db_session:
            m_A = Molecule[m_A].structure
            t_u_sh = Molecule[t_u_sh].structure
        o.put((m_A, t_u_sh, False, index))


if __name__ == '__main__':
    inp = Queue()
    out = Queue()
    for _ in range(10):
        Process(target=worker, args=(inp, out, )).start()

    file = 1
    rank = 1000
    data = []
    for i, id_1 in enumerate(sigma):
        new_id = old_to_new[id_1]
        tshki_1 = set(pairs[id_1])
        total = len(tshki_1)

        t_sh01 = ((iter(set(pairs[new_to_old[n]]) - tshki_1), tshki_1 - set(pairs[new_to_old[n]]), new_to_old[n])
                  for n, x in enumerate(big[new_id]) if x <= 25.5 and new_id != n)
        t_sh45 = ((iter(set(pairs[new_to_old[n]]) - tshki_1), tshki_1 - set(pairs[new_to_old[n]]), new_to_old[n])
                  for n, x in enumerate(big[new_id]) if 102 <= x <= 127.5 and new_id != n)
        t_sh90 = ((iter(set(pairs[new_to_old[n]]) - tshki_1), tshki_1 - set(pairs[new_to_old[n]]), new_to_old[n])
                  for n, x in enumerate(big[new_id]) if x >= 229.5 and new_id != n)

        for triple in islice(unique_everseen(roundrobin2(roundrobin1(t_sh01, t_sh45, t_sh90)), lambda z: z[0]), total):
            t_unic_sh, t_unic, m_A_sh = triple
            inp.put((id_1, m_A_sh, t_unic_sh))
            inp_size = inp.qsize()
            for _ in range(inp_size):
                dt = out.get()
                data.append(dt)
                rank -= 1
                if not rank:
                    with open(f'false/{file}.pickle', 'wb') as wq:
                        dump(data, wq)
                    data = []
                    file += 1
                    rank = 1000

    for _ in range(10):
        inp.put('STOP')
