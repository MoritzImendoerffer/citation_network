import cudf
import cugraph
import pickle
# NetworkX and CPU based libraries

import networkx as nx
import pandas as pd
import hvplot.pandas

from matplotlib import pyplot as plt
from hvplot import hvPlot
import holoviews as hv
# Viz libraries

from cuxfilter.charts.datashader.custom_extensions.graph_assets import calc_connected_edges
import holoviews as hv

from colorcet import fire
from datashader.bundling import directly_connect_edges, hammer_bundle

from holoviews.operation.datashader import datashade, dynspread
from holoviews.operation import decimate

from dask.distributed import Client
# Define the parameters
ITERATIONS = 500
THETA = 1.0
OPTIMIZE = True

with open('./biomass_valorization_results/2021-03-09_23:49:44_biomass valorization.pickle', 'rb') as f:
   g = pickle.load(f)

edge_list = nx.to_edgelist(g)
record = [(item[0], item[1]) for item in edge_list]
sm = nx.to_scipy_sparse_matrix(g)

df = pd.DataFrame.from_records(record)
df.columns = ['source', 'destination']
df_cuda = cudf.DataFrame(df)

G = cugraph.Graph()
G.from_pandas_edgelist(df)
pos_gdf = cugraph.layout.force_atlas2(G,
                                      max_iter=ITERATIONS,
                                      pos_list=None,
                                      outbound_attraction_distribution=True,
                                      lin_log_mode=False,
                                      edge_weight_influence=1.0,
                                      jitter_tolerance=1.0,
                                      barnes_hut_optimize=OPTIMIZE,
                                      barnes_hut_theta=THETA,
                                      scaling_ratio=2.0,
                                      strong_gravity_mode=False,
                                      gravity=1.0,
                                      verbose=False,
                                      callback=None)


# fig, ax = plt.subplots(ncols=1, figsize=(15, 15))
# _p = pos_gdf.loc[:, ['x', 'y']]
# _df = _p.to_arrow()
# _df = _df.to_pandas()
# ax.scatter(x=_df['x'].values, y=_df['y'].values, s=3)
# plt.show()

connected = calc_connected_edges(pos_gdf,
                                 df_cuda,
                                 node_x="x",
                                 node_y="y",
                                 node_x_dtype="float32",
                                 node_y_dtype="float32",
                                 node_id="vertex",
                                 edge_source="source",
                                 edge_target="destination",
                                 edge_aggregate_col=None,
                                 edge_render_type="direct",
                                )
df_conn = connected.to_pandas()


hv.extension('bokeh')
plot = df_conn.hvplot.Scatter(x='x', y='y', datashade=True)
plot