import networkx as nx
import pickle
from matplotlib import pyplot as plt
import numpy as np
# import os
# os.environ["QT_QPA_PLATFORM"] = "wayland"
# from mayavi import mlab

# with open('2021-03-07_21:23:46_digital_twin.pickle', 'rb') as f:
#     g = pickle.load(f)
with open('2021-03-08_11:27:24_biomass valorization.pickle', 'rb') as f:
   g = pickle.load(f)

pos = nx.spring_layout(g)

fig, ax = plt.subplots(ncols=1, figsize=(10, 10), dpi=300)
nx.draw(g, pos=pos, with_labels=False, node_size=0.2, width=0.1, ax=ax)
plt.show()

## 3d Plotting
# reorder nodes from 0,len(G)-1
# G = nx.convert_node_labels_to_integers(g)
# # 3d spring layout
# pos = nx.spring_layout(G, dim=3)
# # numpy array of x,y,z positions in sorted node order
# xyz = np.array([pos[v] for v in sorted(G)])
# # scalar colors
# scalars = np.array(list(G.nodes())) + 5
#
# pts = mlab.points3d(
#     xyz[:, 0],
#     xyz[:, 1],
#     xyz[:, 2],
#     scalars,
#     scale_factor=0.1,
#     scale_mode="none",
#     colormap="Blues",
#     resolution=20,
# )
#
# pts.mlab_source.dataset.lines = np.array(list(G.edges()))
# tube = mlab.pipeline.tube(pts, tube_radius=0.01)
# mlab.pipeline.surface(tube, color=(0.8, 0.8, 0.8))
# mlab.show()