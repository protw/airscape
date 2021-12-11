#!/usr/bin/env python
# coding: utf-8

# #### **Title**: HeatMap Tap stream example
# 
# **Description**: A linked streams example demonstrating how use Tap stream 
# on a HeatMap. The data contains the incidence of measles across US states 
# by year and week (obtained from [Project Tycho](http://www.tycho.pitt.edu)).
# The HeatMap represents the mean measles incidence per year. On tap the 
# Histogram on the right will generate a Histogram of the incidences for each 
# week in the selected year and state.
#
# **Dependencies**: Bokeh
# 
# **Backends**: [Bokeh](./Tap.ipynb)

## Src: http://holoviews.org/reference/streams/bokeh/Tap.html
## Github: https://bit.ly/3doHjSF

import pandas as pd
import panel as pn
import numpy as np
import holoviews as hv
from holoviews import opts

hv.extension('bokeh', width=90)

## Declare dataset
df = pd.read_csv('http://assets.holoviews.org/data/diseases.csv.gz', compression='gzip')
dataset = hv.Dataset(df, vdims=('measles','Measles Incidence'))

## Declare HeatMap
heatmap = hv.HeatMap(dataset.aggregate(['Year', 'State'], np.mean),
          label='Average Weekly Measles Incidence').select(Year=(1928, 2002))

## Declare Tap stream with heatmap as source and initial values
posxy = hv.streams.Tap(source=heatmap, x=1951, y='New York')

## Define function to compute histogram based on tap location
def tap_histogram(x, y):
    return hv.Curve(dataset.select(State=y, Year=int(x)), kdims='Week',
                    label=f'Year: {x}, State: {y}')

## Connect the Tap stream to the tap_histogram callback
tap_dmap = hv.DynamicMap(tap_histogram, streams=[posxy])

## Get the range of the aggregated data we're using for plotting
cmin, cmax = dataset.aggregate(['Year', 'State'], np.mean).range(dim='measles')
## Adjust the min value since log color mapper lower bound must be >0.0
cmin += 0.0000001

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

## Stop server if necessary
#bokeh_server.stop()