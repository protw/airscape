# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 09:18:53 2021

@author: https://protw.github.io/oleghbond
"""

from config_dir import my_dir # first, set paths to my directories

## We're testing a nice paper
## [Python Word Cloud and NLTK | Shep Sheppard](https://sqlshep.com/?p=971)

""" We already read tweets
"""
from twint_ops import twint_query_pars, twint_read_csv

tw = twint_query_pars()
twint_df = twint_read_csv(my_dir['data'] + tw['output_name'])
tweets_ua = twint_df.loc[twint_df['language']=='uk','tweet']
text_ua = ' '.join(tweets_ua)

""" Reading Ukrainian stopwords
"""
import pandas as pd

""" The following Ukrainian words derivative from 'мати' ('to have') are 
    added manually to 'stopwords_ua.txt':
        мав, має, маємо, маєте, мала, мали, мати, матиме, матимемо, 
        матиму, матимеш, маю, мають
"""
stopwords_ua_file = my_dir['data'] + tw['stopwords_ua_file']
stopwords_ua_df = pd.read_csv(stopwords_ua_file, index_col=False, header=None)
stopwords_ua = list(stopwords_ua_df.iloc[:,0])

""" Tokenizing and lemmatizing word list
"""
from nlp_akhmel import ua_tokenizer

tokenized_list = ua_tokenizer(text_ua,ua_stemmer=False,stop_words=stopwords_ua)

import simplemma

langdata = simplemma.load_data('uk')
lemmatized_list = [simplemma.lemmatize(t, langdata) for t in tokenized_list]

""" Building the frequency dictionary from word list
	Src: https://programminghistorian.org/en/lessons/counting-frequencies
"""
def wordListToFreqDict(word_list):
	word_freq = [word_list.count(word) for word in word_list]
	return dict(list(zip(word_list,word_freq)))

word_freq = wordListToFreqDict(lemmatized_list)

""" Sorting dictionary 'word_freq' by value in descending order using 
    function 'sortFreqDict' and saving 'word_freq' in CSV file using 
    function 'dict2csv'. These functions are located in module 'utils'
"""
from utils import sortFreqDict, dict2csv

word_freq = sortFreqDict(word_freq)
csv_file = my_dir['data'] + tw['word_freq_csv']
dict2csv(word_freq, csv_file)

""" We build world cloud 'wrdcld' and simultaneously save it to image
"""
from wordcloud import WordCloud

wrdcld = WordCloud(width=1800, height=1200, background_color='white').\
    generate_from_frequencies(word_freq).to_file(my_dir['data'] + tw['word_freq_img'])
word_freq1 = wrdcld.words_

""" Finally we plot the word cloud
"""
import matplotlib.pyplot as plt

width = 12
height = 8
plt.figure(figsize=(width, height))
plt.imshow(wrdcld)
plt.axis("off")
plt.show()