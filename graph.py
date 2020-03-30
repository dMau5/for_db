from pickle import load, dump
from networkx import DiGraph

# set of building blocks
with open('Acima/ids_of_blocks.pickle', 'rb') as f:
    bb = load(f)

# set of molecules for what count of atoms < 6 atoms
with open('Acima/easy_molecules.pickle', 'rb') as f1:
    easy = load(f1)

# all USPTO reactions dict: key: reaction id, value: dict of reactants and products
with open('Acima/reactions_and_components.pickle', 'rb') as f2:
    data = load(f2)

zinc = bb.union(easy)

# # select all data of reactions from database and save pairs of tuples (ids reactant, ids product)
# with open('Acima/ready_0.pickle', 'wb') as w:
#     dump(al, w)

print('all_reactions -->', (len(data)))

g = DiGraph()
added_reactions = set()
while data:
    r_id, components = data.popitem()
    if r_id in added_reactions:
        continue

    r_node = f'r_{r_id}'
    g.add_node(r_node)
    added_reactions.add(r_id)
    for m in components['products']:
        g.add_edge(r_node, m)
    for m in components['reactants']:
        g.add_edge(m, r_node)
        if m in zinc:
            g.nodes[m]['bb'] = 1
