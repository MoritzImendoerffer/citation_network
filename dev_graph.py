from scholar_classes import MyScholarlyScraper
from scholarly import scholarly
import networkx as nx
import random
import time
import pickle
import datetime

sc = MyScholarlyScraper(search_term='"digital twin" AND "biotechnology"')
# sc = MyScholarlyScraper(search_term='biomass valorization')
sc.load_n_items(10)

def subsequent_iterator(a=0, n=1e3):
    n = int(n)
    for i in range(a, a+n):
        yield i

def get_hash(scholarly_item):
    return hash(scholarly_item['bib']['title'].replace(' ', ''))

g = nx.Graph()
success = 0
fail = 0

for i, active_item in enumerate(sc.active_items):
    print(100 * '=')
    print('Started NX Generation')
    print(100 * '=')
    active_item_id = get_hash(active_item)
    g.add_nodes_from([(active_item_id, {'meta': active_item})])

    # the related and citing articles for the current active article
    related_items = sc.related[i]
    citing_items = sc.cited_by[i]
    if citing_items:
        for citing_item in citing_items:
            # node id for the current related article
            citing_item_id = get_hash(citing_item)
            g.add_nodes_from([(citing_item_id, {'meta': citing_item})])
            g.add_edge(active_item_id, citing_item_id)

    # get the citing artcicles of the related items
    if related_items:
        print(100 * '-')
        print(f'Started iteration through related items')
        print(100 * '-')
        for related_item in related_items:
            # node id for the current related article
            related_item_id = get_hash(related_item)
            g.add_nodes_from([(related_item_id, {'meta': related_item})])
            try:
                related_cited_parser = scholarly.citedby(related_item)
                print(100*'-')
                print('Related Articles: Fetch SUCESS')
                print(100 * '-')
                success += 1
            except Exception as e:
                try:
                    w = random.uniform(1, 2)
                    time.sleep(w)
                    print(f'{i}: Exception: {e} for item {related_item}, retrying')
                    related_cited_parser = scholarly.citedby(related_item)
                    success += 1
                except Exception as e:
                    print(f'{i}: Exception: {e} for item {related_item}')
                    print(100 * '-')
                    print(f'Related Articles: Fetch Failed: {e}')
                    print(100 * '-')
                    fail += 1
                    continue

            related_citing_items = list(related_cited_parser)
            for related_citing_item in related_citing_items:
                # node id for the current citing article
                related_citing_item_id = get_hash(related_citing_item)
                g.add_nodes_from([(related_citing_item_id, {'meta': related_citing_item})])
                g.add_edge(related_item_id, related_citing_item_id)
print(100 * '=')
print('Stopped NX Generation')
print(100 * '=')

from matplotlib import pyplot as plt
fig, ax = plt.subplots(ncols=1, figsize=(10, 10), dpi=300)
pos = nx.spring_layout(g)
nx.draw(g, pos=pos, with_labels=False, node_size=0.2, width=0.1, ax=ax)
plt.show()

with open(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '_' + 'digital_twin.pickle', 'wb') as f:
    pickle.dump(g, f)

