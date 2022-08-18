## Utilities

## Read monitoring data
import pandas as pd
from datetime import datetime

def read_data():
    
    data_file = 'https://raw.githubusercontent.com/protw/airscape/master/' + \
                'data/200421%20Chronograf%20Data.csv'

    df = pd.read_csv(data_file)

    df.time = [datetime.strptime(x[0:19],'%Y-%m-%dT%H:%M:%S') for x in df.time]
    df['dayhour'] = [x.hour for x in df.time]
    df['weekday'] = [x.weekday() for x in df.time]
    df['monthday']= [x.day for x in df.time]
    df['yearday'] = [x.timetuple().tm_yday for x in df.time]
    df['yearweek']= [x.isocalendar()[1] for x in df.time] 
    df['month']   = [x.month for x in df.time] 
    df['year']    = [x.year for x in df.time]

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

    return df, params
