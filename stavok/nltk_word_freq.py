import pandas as pd

from config_dir import my_dir # first, set paths to my directories
from twint_ops import twint_query_pars, twint_read_csv

#### SET TWINT QUERY PARAMETERS

tw = twint_query_pars()

#### TWINT QUERY RESULT PROCESSING

twint_df = twint_read_csv(tw['output_name'])

#### NLP

tweets_ua = twint_df.loc[twint_df['language']=='uk','tweet']

stopwords_ua_file = 'stopwords_ua.txt'
stopwords_ua_df = pd.read_csv(stopwords_ua_file, index_col=False, header=None)
stopwords_ua = list(stopwords_ua_df.iloc[:,0])

from nlp_akhmel import ngrams_info

ngrams_info(tweets_ua, n=1, most_common=20, ua_stemmer=True, \
            stop_words=stopwords_ua)