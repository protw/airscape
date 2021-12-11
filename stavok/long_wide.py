import numpy as np

#from config_dir import my_dir # first, set paths to my directories

## Read monitoring data
from utils import read_data

df = read_data()

## For plotting several data series, reshape dataframe 'val' by pivoting
## See https://pandas.pydata.org/docs/user_guide/reshaping.html
## NOTE: pivot() will error with a 'ValueError: Index contains duplicate 
## entries, cannot reshape' if the index/column pair is not unique. In this 
## case, consider using pivot_table() which is a generalization of pivot that 
## can handle duplicate values for one index/column pair.
df_re = df.pivot_table(index="time", 
                       columns=["sensor_id","factor"], 
                       values="val") 

from datetime import datetime

## Convert index from string format to number in days from the 1st data point
def convert_index(df):
    idt = [datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ') for x in df.index]
    idt = np.array([(x - idt[0]).total_seconds()/3600/24 for x in idt])
    df.set_index(idt,inplace=True)
    df.index.names = ['Days']
    return df

df_re = convert_index(df_re)
#df_re.plot() # For debugging

## Methods are needed for selecting rows and columns in multilevel and 
## multiindexing dataframes (especially after pivoting)!!
## These issues are brilliantly addressed in the following paper:
## https://towardsdatascience.com/accessing-data-in-a-multiindex-dataframe-in-pandas-569e8767201d

## For instance
sensor_id = 9969
df_re_sel = df_re.loc[:,sensor_id] # returns columns `factor = ['PM10', 'PM25']`
## However
factor = 'PM25'
try:
    df_re_sel = df_re.loc[:,factor] # *** KeyError: 'PM25'
except KeyError as ke:
    print(f'KeyError {ke} generated')
## But this works
df_re_sel = df_re.loc[:,(sensor_id,factor)]
## A bit more complex case also works
sensor_id, factor = (9969,10001), ('PM25')
df_re_sel = df_re.loc[:,(sensor_id,factor)]
## Much more complex realisation: factor is on 2nd level (i.e. level=1) and 
## it is a column (i.e. axis=1)
df_re_sel = df_re.xs(factor,level=1,axis=1)

#df_re_sel.plot() # For quick debugging

import plotly.express as px
import plotly.io as pio
pio.renderers.default='browser' # 'browser' or 'svg' or other

## If 'x' is omitted index with its name is taken, otherwise put "x='Days'" 
## into argument list
## If 'y' is omitted all the columns with their names are taken, otherwise 
## put "y=list(df_re_sel.columns)" into argument list
title = f'Concentration of aerosol {factor} (ug/m3) at ' + \
        f'{len(df_re_sel.columns)} locations in Kyiv, Ukraine, ' +\
        f'starting from {df.time[0][:10]}'
fig = px.line(df_re_sel,title=title)
fig.show()


##==== DEPLOYMENT
'''
import streamlit as st
st.line_chart(df_re_sel)
'''
## How to deploy
## [Get started](https://docs.streamlit.io/streamlit-cloud/get-started)
## [Deploy an app](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)
