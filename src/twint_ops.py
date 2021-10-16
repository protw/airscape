## twint operations

#### SET TWINT QUERY PARAMETERS

def twint_query_pars():
    tw = {}
    tw['user'] = 'ZelenskyyUa'
    tw['output_type'] = 'csv'
    tw['output_name'] = './data/twint_zelenski.csv'
    tw['since'] = '2019-04-01'
    return tw

#### FORM QUERY VIA CLI

def twint_cli(tw):
    ## CLI example
    ##!twint -u ZelenskyyUa --since 2019-04-01 -o twint_zelenski.csv --csv

    tw_run_str = 'twint' + \
                 ' -u '  + tw['user'] + \
                 ' --'   + tw['output_type'] + \
                 ' -o '  + tw['output_name']

    return tw_run_str

#### RUN QUERY VIA API

import twint
import nest_asyncio
nest_asyncio.apply()

def twint_api(tw):
    c = twint.Config()

    c.Username = tw['user']
    c.Store_csv = (tw['output_type'] == 'csv')
    c.Output = tw['output_name']
    c.Hide_output = True

    twint.run.Search(c)

    tweets = twint.output.tweets_list

    return len(tweets)

#### TWINT QUERY RESULT PROCESSING

import pandas as pd

def twint_read_csv(twit_file, encode=False, del_empty_cols=False):
    twint_df = pd.read_csv(twit_file, sep=',')

    ## Try to set correct encoding
    if encode:
        twint_df.to_csv(twit_file, sep=',', index=False, \
                        encoding='utf-8-sig')

    ## Delete empty columns
    def del_empty_columns(df):
        df_desc = df.describe().transpose()
        cols_del = df_desc.index.values[df_desc['count'] == 0]
        return df.drop(columns=cols_del, inplace=False)
    if del_empty_cols:    
        twint_df = del_empty_columns(twint_df)
        
    return twint_df
