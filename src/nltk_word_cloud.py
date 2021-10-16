# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 09:18:53 2021

@author: https://protw.github.io/oleghbond
"""

## We're testing a nice paper
## [Python Word Cloud and NLTK | Shep Sheppard](https://sqlshep.com/?p=971)

#### Reading Ukrainian stopwords

import pandas as pd

stopwords_ua_file = 'stopwords_ua.txt'
stopwords_ua_df = pd.read_csv(stopwords_ua_file, index_col=False, header=None)
stopwords_ua = list(stopwords_ua_df.iloc[:,0])

#### We already read tweets

from twint_ops import twint_query_pars, twint_read_csv

tw = twint_query_pars()
twint_df = twint_read_csv(tw['output_name'])
tweets_ua = twint_df.loc[twint_df['language']=='uk','tweet']
text_ua = ' '.join(tweets_ua)

from nlp_akhmel import ua_tokenizer

tokenized_list = ua_tokenizer(text_ua,ua_stemmer=True,stop_words=stopwords_ua)

'''
wordcloud = WordCloud(width=1800,height=1200, background_color='white'). \
    generate_from_frequencies(word_freq)

#### First we create the word frequency dictionary 'word_freq'

word_freq = worldcloud.words_

#### Then we manually correct the word frequency dictionary 'word_freq' 
#### and prepare corrected version of 'word_freq' in 'word_freq_zel_2.py'
'''

#### We build world cloud 'wrdcld' and simultaneously save it to image
#### 'word_freq_zel.png'

from word_freq_zel_2 import word_freq
from wordcloud import WordCloud

wrdcld = WordCloud(width=1800, height=1200, background_color='white').\
    generate_from_frequencies(word_freq).to_file('word_freq_zel.png')

#### Finally we plot the word cloud

import matplotlib.pyplot as plt

width = 12
height = 8
plt.figure(figsize=(width, height))
plt.imshow(wrdcld)
plt.axis("off")
plt.show()