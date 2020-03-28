from pickle import load, dump
from pony.orm import db_session, select
# from CGRtools.containers import ReactionContainer, MoleculeContainer
# from CGRtools.files import SDFread, RDFread, SDFwrite, RDFwrite
# from multiprocessing import Process, Queue
# # from CGRdbUser import User
# from CGRdb import load_schema, Molecule, Reaction


# set of building blocks
with open('Acima/ids_of_blocks.pickle', 'rb') as f:
    bb = load(f)

# set of molecules for what count of atoms < 6 atoms
with open('Acima/easy_molecules.pickle', 'rb') as f1:
    easy = load(f1)

# all USPTO reactions dict: key: reaction id, value: dict of reactants and products
with open('Acima/reactions_and_components.pickle', 'rb') as f2:
    data = load(f2)

al = bb.union(easy)

# select all data of reactions from database and save pairs of tuples (ids reactant, ids product)
with open('Acima/ready_0.pickle', 'wb') as w:
    dump(al, w)


with db_session:
    print('all_reactions -->', (len(data)))

    n = 1
    while data:
        dt = data.copy()
        now = set()
        for i, r in enumerate(dt.items()):
            r_id, components = r
            if set(components['reactants']) <= al:
                data.pop(r_id)
                for m in components['products']:
                    now.add(m)
            if not i % 1000:
                print('done', i)

        if now:
            now = now - al
            with open(f'Acima/ready_{n}.pickle', 'wb') as w1:
                dump(now, w1)
            with open(f'Acima/balance_{n}.pickle', 'wb') as w2:
                dump(data, w2)
            al = al.union(now)
            print('cycle -->', n)
            print('common_reactions -->', len(data))
            n += 1
        else:
            for r_id, components in dt.items():
                data.pop(r_id)
                for m in components['products']:
                    if m not in al:
                        now.add(m)
            with open('Acima/ready_None.pickle', 'wb') as w2:
                dump(now, w2)
            break
