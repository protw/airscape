## Аналіз твітів з допомогою *Twint*

## USEFULL DISCUSSION https://github.com/twintproject/twint/issues/1111
## [рішення проблеми](https://github.com/twintproject/twint/issues/1253#issuecomment-913055717

#### SET TWINT QUERY PARAMETERS

def twint_query_pars():
    tw = {}
    tw['user'] = 'ZelenskyyUa'
    tw['output_type'] = 'csv'
    tw['output_name'] = 'twint_zelenski.csv'
    tw['since'] = '2019-04-01'
    return tw

tw = twint_query_pars()

#### RUN QUERY VIA CLI

import os

def twint_cli(tw):

    #!twint -u ZelenskyyUa --since 2019-04-01 -o twint_zelenski.csv --csv
    tw_run_str = 'twint' + \
                 ' -u '  + tw['user'] + \
                 ' --'   + tw['output_type'] + \
                 ' -o '  + tw['output_name']
    return tw_run_str

tw_run_str = twint_cli(tw)
#os.system(tw_run_str) # uncomment if necessary

#### RUN QUERY VIA API

import twint
import nest_asyncio
nest_asyncio.apply()

def twint_api(tw):
    c = twint.Config()

    c.Username = tw['user']
    c.Store_csv = (tw['output_type'] == 'csv')
    c.Output = tw['output_name']

    twint.run.Search(c)

    tweets = twint.output.tweets_list
    len(tweets)
    return

#twint_api() # uncomment if necessary

#### TWINT QUERY RESULT PROCESSING

import pandas as pd

twint_df = pd.read_csv(tw['output_name'], sep='\t')

def del_empty_columns(df):
    df_desc = df.describe().transpose()
    cols_del = df_desc.index.values[df_desc['count'] == 0]
    return df.drop(columns=cols_del, inplace=False)

twint_df = del_empty_columns(twint_df)
