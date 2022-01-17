import datashader as ds, pandas as pd, colorcet as cc

taxi_data = 'https://raw.githubusercontent.com/holoviz/datashader/master/' +\
    'examples/data/.data_stubs/nyc_taxi.csv'

df = pd.read_csv(taxi_data, usecols=['dropoff_x', 'dropoff_y'])
df.head()

import holoviews as hv
from holoviews.element.tiles import EsriImagery
from holoviews.operation.datashader import datashade
hv.extension('bokeh')

import panel as pn
pn.extension()


map_tiles  = EsriImagery().opts(alpha=0.5, width=900, height=480, bgcolor='black')
points     = hv.Points(df, ['dropoff_x', 'dropoff_y'])
taxi_trips = datashade(points, x_sampling=1, y_sampling=1, cmap=cc.fire, width=900, height=480)

pn.Row(map_tiles * taxi_trips).show()