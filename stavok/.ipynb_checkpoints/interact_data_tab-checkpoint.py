# # Демонстрація інтерактивних даних
# 
# Ця демонстрація працює в Jupyter Notebook на локальному комп'ютері

import numpy as np
from utils import read_data
import panel as pn
import holoviews as hv
from holoviews import opts

pn.extension()
hv.extension('bokeh')

#### Get data

df, params = read_data()

dataset = hv.Dataset(df, 
                     kdims=[('sensor_id','№ датчика'),
                            ('time','Час, крок 30 хв'),
                            ('yearday','День року'),
                            ('dayhour','Година доби'),
                            ('weekday','День тижня'),
                            ('factor','Фактор забруднення')],
                     vdims=('val','Концентрація, µг/м3'))

#### Declare Panel of parameters 'param_panel'

date_range_slider = pn.widgets.DateRangeSlider(name='Діапазон дат',
    start=params['time'][0], end=params['time'][1],
    value=(params['time'][0], params['time'][1]))

sns_radio = pn.widgets.RadioBoxGroup(name='SensorRadio', width=100, 
                                     options=params['sensors'], inline=False)
fct_radio = pn.widgets.RadioBoxGroup(name='FactorRadio', width=100,
                                     options=params['factors'], inline=False)

sns_radio_label = pn.widgets.StaticText(name='№ датчика', value='', width=100)
fct_radio_label = pn.widgets.StaticText(name='Фактор', value='', width=100)

param_panel = pn.Row(date_range_slider, pn.Column(sns_radio_label, sns_radio), 
                     pn.Column(fct_radio_label, fct_radio))

#### Declare Tabs panel of diagrams 'info_viz'

# Проблема: [Panel Tabs as item in panel Column switches to first tab on widget 
# interactions](https://bit.ly/3nf96KC)
# Рішення: введення статичного об'єкту Tabs_Panel, під час взаємодії 
# змінюються його компоненти, але не сам об'єкт

Tabs_Panel = pn.Tabs([],[])

@pn.depends(date_range_slider.param.value, sns_radio.param.value, 
            fct_radio.param.value)
def info_viz(drs,sns,fct):
  dss = dataset.select(time=drs, sensor_id=sns, factor=fct)
  crv = hv.Curve(dss, kdims='time', label=f'Датчик: {sns}, Фактор: {fct},'
                   f' Від: {drs[0]}, До: {drs[1]}', name='Часовий ряд')
  crv.opts(opts.Curve(width=800, show_grid=True, xlabel='Time, 30 min step'))

  dss = dss.aggregate(['dayhour', 'weekday'], np.mean)
  yticks = [(0, 'Mon'), (1, 'Tue'), (2, 'Wed'), (3, 'Thu'), 
            (4, 'Fri'), (5, 'Sat'), (6, 'Sun')]
  hm = hv.HeatMap(dss, label='Київ, Січ-Кві 2020 (датчики Airly)', 
                  name='Тиждень-доба')
  hm.opts(opts.HeatMap(tools=['hover'], colorbar=True, ylabel='День тижня',
                       xlabel='Година дня', clabel='Концентрація, µг/м3',
                       width=500, yticks=yticks, fontsize={'title': 11}))
  Tabs_Panel[0] = crv
  Tabs_Panel[1] = hm
  
  return Tabs_Panel

#### Compose panels and render

pn.Column(param_panel, info_viz)

bokeh_server = pn.Column(param_panel, info_viz).show(port=12346)
# bokeh_server.stop()

# ### Як серверний веб-застосунок
#   ```
#     (base)> activate airscape
#     (airscape)> panel serve interact_data_tab.py
#     
#     http://localhost:5006/interact_data_tab
#   ```




