# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 20:53:17 2021

@author: oleghbond, https://github.com/protw/airscape
"""

## За мотивами статті Андрія Хмельницького [Перші кроки в NLP: розглядаємо 
## Python-бібліотеку NLTK в реальному завданні | DOU]
## (https://dou.ua/lenta/articles/first-steps-in-nlp-nltk/)

import re
import nltk
nltk.download('punkt')
from ukrainian_stemmer import UkrainianStemmer

def ua_tokenizer(text,ua_stemmer=True,stop_words=[]):
    """ Tokenizer for Ukrainian language, returns only alphabetic tokens.
    
    Keyword arguments:
    text -- text for tokenize
    ua_stemmer -- if True use UkrainianStemmer for stemming words (default True)
    stop_words -- list of stop words (default [])
    """
    tokenized_list=[]
    text = re.sub(r"http\S+", "", text) #remove urls
    text=re.sub(r'\S+\.com\S+','',text) #remove urls
    text=re.sub(r'\@\w+','',text) #remove mentions
    text =re.sub(r'\#\w+','',text) #remove hashtags

    text=re.sub(r"""['’"`«»]""", '', text)
    text=re.sub(r"""([0-9])([\u0400-\u04FF]|[A-z])""", r"\1 \2", text)
    text=re.sub(r"""([\u0400-\u04FF]|[A-z])([0-9])""", r"\1 \2", text)
    text=re.sub(r"""[\-–.,!:+*/_]""", ' ', text)
    
    for word in nltk.word_tokenize(text):
        if word.isalpha():
            word=word.lower()
        else:
            continue
        if ua_stemmer is True:
            word=UkrainianStemmer(word).stem_word()
        if word not in stop_words:    
            tokenized_list.append(word)
    return tokenized_list

def ngrams_info(series,n=1,most_common=20,ua_stemmer=True,stop_words=[]):
    """ ngrams_info - Show detailed information about string pandas.Series column.
    
    Keyword arguments:
    series -- pandas.Series object
    most_common -- show most common words(default 50)
    ua_stemmer -- if True use UkrainianStemmer for stemming words (default True)
    stop_words -- list of stop words (default [])
   	 
    """
    words=series.str.cat(sep=' ')
    print ('Кількість символів: ',len(words))
    tokenized_list = ua_tokenizer(words, ua_stemmer=ua_stemmer, \
                                  stop_words=stop_words)
    words=nltk.ngrams(tokenized_list, n)
    words=nltk.FreqDist(words)
    print ('Кількість токенів: ',words.N())
    print ('Кількість унікальних токенів: ',words.B())
    print ('Найбільш уживані токени: ',words.most_common(most_common))
    words.plot (most_common, cumulative = True)
