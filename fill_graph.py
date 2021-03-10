"""
A graph will, at first, contain unconnected nodes, because scraping failed. This skript takes an already
existing graph and fill it up
"""

from scholar_classes import MyScholarlyScraper, get_cited_by
from scholarly import scholarly
import networkx as nx
import random
import time
import pickle
import datetime
import concurrent

'''
Funktioniert. 
TODO: 
1) Liste mit papers EXTEND liste mit related 
2) `get_citations` und `fill` über alle einträge aus 1. 
Wichtig: alles operiert nur auf Liste aus 1
'''

file_name_graph = '2021-03-07_21:23:46_digital_twin.pickle'

with open(file_name_graph, 'rb') as f:
    g = pickle.load(f)

def get_hash(scholarly_item):
    return hash(scholarly_item['bib']['title'].replace(' ', ''))

# degree of each node (node name, degree)
deg = [(node_hash, g.degree[node_hash]) for node_hash in g.nodes.keys()]
# from smalles to largest degree of nodes
deg.sort(key = lambda x: x[1])

sc = None
for i, node_item in enumerate(deg):
    print(100 * '=')
    print('Started Graph fill')
    print(100 * '=')
    node_hash, degree = node_item


    # the related and citing articles for the current active article (since they are already sorted, simple indexing
    # is enough). Looks like [(index, [{}, {}, ...], success message), ...]
    related_items = sc.related[i]
    citing_items = sc.cited_by[i]
    if citing_items[2]:
        for citing_item in citing_items[1]:
            # node id for the current related article
            citing_item_id = get_hash(citing_item)
            g.add_nodes_from([(citing_item_id, {'meta': citing_item})])
            g.add_edge(active_item_id, citing_item_id)

    # get the citing artcicles of the related items
    if related_items[2]:
        print(100 * '-')
        print(f'Started iteration through related items')
        print(100 * '-')
        if related_items[1]:
            for related_item in related_items[1]:
                # node id for the current related article
                related_item_id = get_hash(related_item)
                g.add_nodes_from([(related_item_id, {'meta': related_item})])

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                # a bit hacky but I have to add the index (related_item[0]) to the call, although it is the same for
                # all items
                related_citations_list = list(executor.map(lambda item: get_cited_by((related_items[0], item)), related_items[1]))

            # related citations list looks like (index, [{}, {}, ...], success)
            for related_citing_item in related_citations_list:
                if related_citing_item[2]:  # success
                    # node id for the current citing article
                    if related_citing_item[1]:  # list could be empty
                        for rel_item in related_citing_item[1]:
                            related_citing_item_id = get_hash(rel_item)
                            g.add_nodes_from([(related_citing_item_id, {'meta': related_citing_item})])
                            g.add_edge(related_item_id, related_citing_item_id)

print(100 * '=')
print('Stopped NX Generation')
print(100 * '=')

with open(file_name_graph, 'wb') as f:
    pickle.dump(g, f)
with open(file_name_sc, 'wb') as f:
    pickle.dump(sc, f)

