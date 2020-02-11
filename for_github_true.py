from CGRdb import load_schema
from CGRdb.database import Molecule
from pony.orm import db_session
from pickle import dump, load


load_schema('name', user='postgres', password='pass', host='host', database='postgres')

with open('pairs_from_reactant_to_product.pickle', 'rb') as f:
    pairs = load(f)

trues = []
rank = 1000
file = 1
for reactant_id, value in pairs.items():
    with db_session:
        reactant = Molecule[reactant_id].structure
        for product in Molecule.select(lambda x: x.id in value.keys()):
            r_id, stages = value[product.id]
            trues.append((reactant, product.structure, True, stages))
            rank -= 1
            if not rank:
                with open(f'rues/{file}.pickle', 'wb') as ww:
                    dump(trues, ww)
                rank = 1000
                file += 1
                trues = []
