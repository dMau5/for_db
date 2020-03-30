from pickle import load, dump
from networkx import DiGraph

# # set of building blocks
# with open('Acima/ids_of_blocks.pickle', 'rb') as f:
#     bb = load(f)
#
# # set of molecules for what count of atoms < 6 atoms
# with open('Acima/easy_molecules.pickle', 'rb') as f1:
#     easy = load(f1)
#
# # all USPTO reactions dict: key: reaction id, value: dict of reactants and products
# with open('Acima/reactions_and_components.pickle', 'rb') as f2:
#     data = load(f2)
#
# zinc = bb.union(easy)
#
# print('all_reactions -->', (len(data)))

# g = DiGraph()
# added_reactions = set()
# while data:
#     r_id, components = data.popitem()
#     if r_id in added_reactions:
#         continue
#
#     r_node = f'r_{r_id}'
#     g.add_node(r_node)
#     added_reactions.add(r_id)
#     for m in components['products']:
#         g.add_edge(r_node, m)
#     for m in components['reactants']:
#         g.add_edge(m, r_node)
#         if m in zinc:
#             g.nodes[m]['bb'] = 1
with open('USPTO_graph.pickle', 'rb') as q:
    gg = load(q)

g = DiGraph(gg)
while True:
    remove = []
    for x in g.nodes():
        if isinstance(x, int):
            if 'bb' in g.nodes[x]:
                continue
            if not g._pred[x]:
                remove.append(x)
    if remove:
        for rm in remove:
            succ = g._succ[rm]
            g.remove_node(rm)
            g.remove_nodes_from(succ)
    else:
        break
with open('update_graph.pickle', 'wb') as u:
    dump(g, u)
