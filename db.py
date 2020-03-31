from pickle import load, dump
from pony.orm import db_session
from CGRdb import Molecule


n = 0
size = 1000
data = []
common = 0
c = set()
for stage in range(8):
    print('stage', stage)
    with open(f'Acima/graph_{stage}.pickle', 'rb') as f:
        mols = load(f)
        common += len(mols)
        c = c.union(mols)
        with db_session:
            for m in Molecule.select(lambda x: x.id in mols):
                data.append((m.structure, stage))
                if len(data) == 1000:
                    with open(f'dataset/{n}.pickle', 'wb') as f1:
                        dump(data, f1)
                        n += 1
                        data = []

with open(f'Acima/graph_None.pickle', 'rb') as f2:
    mos = load(f2)
    common += len(mos)
    c = c.union(mos)
    print('file -->', None)
    with db_session:
        for mol in Molecule.select(lambda x: x.id in mos):
            data.append((mol.structure, None))
            if len(data) == 1000:
                with open(f'dataset/{n}.pickle', 'wb') as f3:
                    dump(data, f3)
                    n += 1
                    data = []
print(common)
print('ff', len(c))
print('file -->')

# ______

for stage in range(8):
    # print('stage', stage)
    with open(f'Acima/graph_{stage}.pickle', 'rb') as f:
        mols = load(f)
    for stag in range(8):
        if stage == stag:
            continue
        # print('stage', stag)
        with open(f'Acima/graph_{stag}.pickle', 'rb') as f1:
            ms = load(f1)
        ie = mols.intersection(ms)
        print(stage, stag, 'inter', len(ie))

# print('None')
with open(f'Acima/graph_None.pickle', 'rb') as f2:
    mos = load(f2)
    for st in range(8):
        # print('stage', st)
        with open(f'Acima/graph_{st}.pickle', 'rb') as f3:
            s = load(f3)
        ie = mos.intersection(s)
        print(None, st, 'inter', len(ie))
exit()
