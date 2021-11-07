import twint
import pandas as pd

import nest_asyncio
nest_asyncio.apply()

cities = [
    {'c':'kyiv',  'l':['uk','ru']},
    {'c':'krakow','l':['']},
    {'c':'london','l':['en']}]
start_time = '2021-09-25'
end_time = '2021-09-26'

def read_save_twits(city,lang):
    c = twint.Config()

    c.Near         = city
    c.Since        = start_time
    c.Until        = end_time
    c.Hide_output  = True
    c.Count        = True
    c.Pandas       = True
    c.Store_pandas = True
    if lang != 'all':
        c.Lang     = lang

    twint.run.Search(c)

    Tweets_df = twint.storage.panda.Tweets_df
    
    num_of_tweets = len(Tweets_df)
    if num_of_tweets != 0:
        file = f"{''.join(start_time.split('-'))[2:8]}-{city}-{lang}.csv" 
        Tweets_df.to_csv(file, sep=',', decimal='.', encoding="utf-8-sig",
                         index=False)
    return num_of_tweets

for city in cities:
    c = city['c']
    for lang in city['l']:
        if len(lang) == 0: 
            lang = 'all'
        num_of_tweets = read_save_twits(c,lang)
        print(f'Місто: {c}, мова: {lang} - {num_of_tweets} твітів')

"""
c.Lang = 'uk' # does not work

To correct the bug it is necessary to insert into line 113 of url.py the 
following code:

    if config.Lang:
        q += f" lang:{config.Lang}"
"""
'''
#c.Search    = 'повітря OR повітрям OR повітрю OR повітрі'
#c.Geo       = '50.450199,30.524105,200km'
#c.Store_csv = True
#c.Output    = f'210925-{c.Near}.csv'

CRITICAL:root:twint.run:Twint:Feed:noData'globalObjects'
sleeping for 1.0 secs
CRITICAL:root:twint.run:Twint:Feed:noData'globalObjects'
sleeping for 8.0 secs'''