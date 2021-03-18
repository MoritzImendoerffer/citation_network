import networkx as nx
import pickle
import numpy as np
import sknetwork as sn
from IPython.display import SVG, display, display_svg,
# with open('2021-03-07_21:23:46_digital_twin.pickle', 'rb') as f:
#     g = pickle.load(f)
with open('./biomass_valorization_results/2021-03-09_23:49:44_biomass valorization.pickle', 'rb') as f:
   g = pickle.load(f)

## Unless,
csr = nx.to_scipy_sparse_matrix(g)
img = sn.visualization.svg_graph(csr, node_size=1, filename='test.svg')
# svg_img = SVG(img)
#
# with open('test.svg' , 'w') as f:
#    for line in svg_img.data:
#       f.write(line)