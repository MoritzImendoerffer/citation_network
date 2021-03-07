from scholar_classes import MyScholarlyScraper, get_cited_by
from scholarly import scholarly
import networkx as nx
import random
import time
import pickle
import datetime
import concurrent

sc = MyScholarlyScraper(search_term='"digital twin" AND "biotechnology"')
# sc = MyScholarlyScraper(search_term='biomass valorization')
sc.load_n_items(20)

def subsequent_iterator(a=0, n=1e3):
    n = int(n)
    for i in range(a, a+n):
        yield i

def get_hash(scholarly_item):
    return hash(scholarly_item['bib']['title'].replace(' ', ''))

g = nx.Graph()

for i, active_item in enumerate(sc.active_items):
    print(100 * '=')
    print('Started NX Generation')
    print(100 * '=')
    active_item_id = get_hash(active_item[1])
    g.add_nodes_from([(active_item_id, {'meta': active_item})])

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

from matplotlib import pyplot as plt
fig, ax = plt.subplots(ncols=1, figsize=(20, 20), dpi=300)
pos = nx.spring_layout(g)
nx.draw(g, pos=pos, with_labels=False, node_size=0.2, width=0.1, ax=ax)
plt.show()

with open(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '_' + 'digital_twin.pickle', 'wb') as f:
    pickle.dump(g, f)

