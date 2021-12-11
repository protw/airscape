#!/usr/bin/env python
# coding: utf-8
"""
 #### **Title**: HeatMap Tap stream example
 
 **Description**: A linked streams example demonstrating how use Tap stream 
 on a HeatMap. The data contains aerosol (PM) concentration every 30 min
 for 4 sensors and for 2 PM size ranges - 2.5 and 10 .
 The HeatMap represents the mean measles incidence per year. On tap the 
 Histogram on the right will generate a Histogram of the incidences for each 
 week in the selected year and state.

 **Dependencies**: Bokeh
 **Backends**: [Bokeh](./Tap.ipynb)

 #### **To launch as a server:**

    > panel serve Tap_air.py

 After that you'll be asked to go to the browser and launch the app from 
 the web-address bar:

    http://localhost:5006/Tap_air

# Ref src: http://holoviews.org/reference/streams/bokeh/Tap.html
# Ref github: https://bit.ly/3doHjSF
"""

"""
!conda install -c pyviz holoviz
"""

import panel as pn
import numpy as np
import holoviews as hv
from holoviews import opts

hv.extension('bokeh', width=90)

## Read monitoring data
from utils import read_data
df = read_data()
df.sensor_id = [str(x) for x in df.sensor_id]

## Declare dataset
dataset = hv.Dataset(df, 
                     kdims=[('sensor_id','Sensor #'),
                            ('yearday','Day of a year'),
                            ('dayhour','Hour of a day'),
                            ('factor','Pollution factor')],
                     vdims=('val','Concentration, µg/m3'))

## extrema
xmin = df.yearday.min()
xmax = df.yearday.max()
ymin = df.sensor_id.min()
factors = df.factor.unique()
factor = factors[0]

## Declare HeatMap
heatmap = hv.HeatMap(dataset.aggregate(['yearday', 'sensor_id'], np.mean),
      label=f'Avg Daily {factor} Concentration').select(yearday=(xmin, xmax))

## Declare Tap stream with heatmap as source and initial values
posxy = hv.streams.Tap(source=heatmap, x=xmin, y=ymin)

## Define function to compute histogram based on tap location
def tap_histogram(x, y):
    return hv.Curve(dataset.select(sensor_id=y, yearday=int(x), factor=factor), 
                    kdims='dayhour', label=f'Day of year: {int(x)}, Sensor: {y}')

## Connect the Tap stream to the tap_histogram callback
tap_dmap = hv.DynamicMap(tap_histogram, streams=[posxy])

## Get the range of the aggregated data we're using for plotting
cmin, cmax = dataset.aggregate(['yearday', 'sensor_id'], np.mean).range(dim='val')
## Adjust the min value since log color mapper lower bound must be >0.0

## Display the Heatmap and Curve side by side
heatmap_tap_dmap = heatmap + tap_dmap
(heatmap_tap_dmap).opts(
    opts.Curve(framewise=True, height=500, line_color='black', width=375, 
               yaxis='right'),
    opts.HeatMap(clim=(cmin, cmax), cmap='RdBu_r', fontsize={'xticks': '6pt'}, 
             height=500, logz=True, tools=['hover'], width=700, xrotation=90))

## Rendering plot in Spyder
## https://stackoverflow.com/a/57971346

import panel as pn

bokeh_server = pn.Row(heatmap_tap_dmap).show(port=12346)

## Stop server if necessary !!!!
#bokeh_server.stop()