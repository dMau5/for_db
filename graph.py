from pickle import load, dump
from networkx import DiGraph

# set of building blocks
with open('Acima/ids_of_blocks.pickle', 'rb') as f:
    bb = load(f)

# set of molecules for what count of atoms < 6 atoms
with open('Acima/easy_molecules.pickle', 'rb') as f1:
    easy = load(f1)
#
# # all USPTO reactions dict: key: reaction id, value: dict of reactants and products
# with open('Acima/reactions_and_components.pickle', 'rb') as f2:
#     data = load(f2)
#
zinc = bb.union(easy)
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
# with open('USPTO_graph.pickle', 'rb') as q:
#     gg = load(q)
#
# g = DiGraph(gg)
# while True:
#     remove = []
#     for x in g.nodes():
#         if isinstance(x, int):
#             if 'bb' in g.nodes[x]:
#                 continue
#             if not g._pred[x]:
#                 remove.append(x)
#     if remove:
#         for rm in remove:
#             succ = g._succ[rm]
#             g.remove_node(rm)
#             g.remove_nodes_from(succ)
#     else:
#         break

# g = DiGraph(gg)
# rm = []
# for x in g.nodes():
#     if isinstance(x, int) and not g._pred[x] and not g._succ[x]:
#         rm.append(x)
# print(len(rm))
# g.remove_nodes_from(rm)
# with open('update_graph.pickle', 'wb') as w:
#     dump(g, w)

# stage = 1
# seen = set()
# stack = [(x, 0) for x in zinc if x in g]
# res = stack.copy()
# while stack:
#     mt, st = stack.pop(0)
#     st += 1
#     scc = g._succ[mt]
#     if scc:
#         for r in scc:
#             if r not in seen:
#                 seen.add(r)
#                 for p in g._succ[r]:
#                     stack.append((p, st))
#                     res.append((p, st))
#
#     print('stage', stage)
#     if st_reactants:
#         with open(f'Acima/graph_all.pickle', 'wb') as w1:
#             dump(st_reactants, w1)
#         zinc = st_reactants.copy()
#         stage += 1
#     else:
#         break

with open('USPTO_graph.pickle', 'rb') as q:
    big_g = load(q)
with open('update_graph.pickle', 'rb') as u:
    g = load(u)

stage = 1
seen_r = set()
seen_m = zinc.copy()
z = zinc.copy()
while True:
    st_reactants = set()
    for m in z:
        if m in g:
            scc = g._succ[m]
            if scc:
                for r in scc:
                    if r not in seen_r:
                        seen_r.add(r)
                        for p in g._succ[r]:
                            if p not in seen_m:
                                seen_m.add(p)
                                st_reactants.add(p)
    print('stage', stage)
    if st_reactants:
        with open(f'Acima/graph_{stage}.pickle', 'wb') as w1:
            dump(st_reactants, w1)
        z = st_reactants.copy()
        stage += 1
    else:
        break
n = set()
print('None')
for x in big_g.nodes():
    if isinstance(x, int) and x not in g:
        n.add(x)
with open(f'Acima/graph_None.pickle', 'wb') as w2:
    dump(n, w2)

with open(f'Acima/graph_0.pickle', 'wb') as w2:
    dump(set(x for x in zinc if x in g), w2)


common = 0
c = set()
for x in range(8):
    with open(f'Acima/graph_{x}.pickle', 'rb') as w1:
        d = load(w1)
        common += len(d)
        c = c.union(d)
with open(f'Acima/graph_None.pickle', 'rb') as w2:
    d = load(w2)
    common += len(d)
    c = c.union(d)
print('ff', common)
print(len(c))
