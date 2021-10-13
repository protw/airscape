import pandas as pd

#### SET TWINT QUERY PARAMETERS

def twint_query_pars():
    tw = {}
    tw['user'] = 'ZelenskyyUa'
    tw['output_type'] = 'csv'
    tw['output_name'] = './data/twint_zelenski.csv'
    tw['since'] = '2019-04-01'
    return tw

tw = twint_query_pars()

#### TWINT QUERY RESULT PROCESSING

twint_df = pd.read_csv(tw['output_name'], sep='\t')

def del_empty_columns(df):
    df_desc = df.describe().transpose()
    cols_del = df_desc.index.values[df_desc['count'] == 0]
    return df.drop(columns=cols_del, inplace=False)

twint_df = del_empty_columns(twint_df)

#### NLP

from nlp_akhmel import *

tweets_ua = twint_df.loc[twint_df['language']=='uk','tweet']

stopwords_ua_file = 'stopwords_ua.txt'
stopwords_ua_df = pd.read_csv(stopwords_ua_file, index_col=False, header=0)
stopwords_ua = stopwords_ua_df.iloc[0,:]

ngrams_info(tweets_ua, n=1, most_common=20, ua_stemmer=True, \
            stop_words=stopwords_ua)