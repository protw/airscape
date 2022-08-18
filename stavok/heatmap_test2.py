import numpy as np
import holoviews as hv
from holoviews import opts
hv.extension('bokeh')
import panel as pn
from utils import read_data

#data = [(i, chr(97+j),  i*j) for i in range(5) for j in range(5) if i!=j]

#bokeh_server = pn.Row(hm).show(port=12346)

df = read_data()

params = {
    'factors': sorted(df.factor.unique()),
    'sensors': sorted(df.sensor_id.unique()),
    'time': [df.time.min(), df.time.max()],
    'values': [df.val.min(), df.val.max()],
    'hours_in_day': sorted(df.dayhour.unique()),
    'days_in_week': sorted(df.weekday.unique()),
    'days_in_month': sorted(df.monthday.unique()),
    'day_in_year': sorted(df.yearday.unique()),
    'week_in_year': sorted(df.yearweek.unique()),
    'month_in_year': sorted(df.month.unique())
}

fct, sns = params['factors'][0], params['sensors'][0]

dataset = hv.Dataset(df, 
                     kdims=[('sensor_id','Sensor #'),
                            ('time','Time, 30 min step'),
                            ('yearday','Day of a year'),
                            ('dayhour','Hour of a day'),
                            ('weekday','Day of a week'),
                            ('factor','Pollution factor')],
                     vdims=('val','Concentration, µg/m3'))

data_sel = dataset.select(sensor_id=sns, factor=fct)
data_sel = data_sel.aggregate(['dayhour', 'weekday'], np.mean)

yticks = [(0, 'Mon'), (1, 'Tue'), (2, 'Wed'), (3, 'Thu'), 
          (4, 'Fri'), (5, 'Sat'), (6, 'Sun')]

hm = hv.HeatMap(data_sel, label='Kyiv, Jan-Apr 2020 (Airly sensors)')
hm.opts(opts.HeatMap(tools=['hover'],
                     colorbar=True,
                     clabel='PM concentration, ug/m3',
                     ylabel='Day of a week',
                     xlabel='Hour of a day',
                     width=500,
                     yticks=yticks,
                     fontsize={'title': 11}
                     ))

bokeh_server = pn.Row(hm).show(port=12346)
#bokeh_server.stop()
