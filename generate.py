from pickle import load, dump
from pony.orm import db_session, select
from CGRtools.containers import ReactionContainer, MoleculeContainer
from CGRtools.files import SDFread, RDFread, SDFwrite, RDFwrite
from multiprocessing import Process, Queue
# from CGRdbUser import User
from CGRdb import load_schema, Molecule, Reaction

with open('Acima/ids_of_blocks.pickle', 'rb') as f:
    bb = load(f)
    tree = {k: 0 for k in bb}

# select all data of reactions from database and save pairs of tuples (ids reactant, ids product)
with open('Acima/ready_0.pickle', 'wb') as w:
    dump(set(tree), w)

al = set(tree)
with db_session:
    data = [x for x in Reaction.select()]
    print('all_reactions -->', (len(data)))

    n = 1
    while data:
        dt = data.copy()
        now = set()
        for i, r in enumerate(dt):
            reacts = set()
            produc = []
            for m in r.molecules:
                mol = m.molecule
                if not m.is_product:
                    atoms = [atom[-1].element for atom in mol.structure.atoms()]
                    if atoms.count('C') <= 2 or len(atoms) <= 6:
                        continue
                    else:
                        reacts.add(mol.id)
                else:
                    produc.append(mol.id)
            if not reacts or reacts <= al:
                data.remove(r)
                for m in produc:
                    now.add(m)
            if not i % 1000:
                print('done', i)
        if now:
            for m in now:
                if m in al:
                    now.remove(m)
            with open(f'Acima/ready_{n}.pickle', 'wb') as w1:
                dump(now, w1)
            al.union(now)
            print('cycle -->', n)
            print('common_reactions -->', len(data))
            n += 1
        else:
            for r in dt:
                data.remove(r)
                for m in r.molecules:
                    if m.is_produst:
                        idd = m.id
                        if idd not in al:
                            now.add(idd)
            with open('Acima/ready_None.pickle', 'wb') as w2:
                dump(now, w2)
            break