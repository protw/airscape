import pandas as pd

from config_dir import my_dir # first, set paths to my directories

## Read all twits marked with categories
twits = my_dir['data'] + 'twint_zelenski_categ.csv'
twits_df = pd.read_csv(twits)

## Join three categories [3,6,7] into single [3]
twits_df['Категорія_Ід2'] = \
    [(3 if x in [1,6,7] else x) for x in twits_df['Категорія_Ід']]
twits_df['Категорія_Ід2'] = \
    [(4 if x in [5] else x) for x in twits_df['Категорія_Ід2']]

## Read definitions of categores
categ = my_dir['data'] + 'twint_zelenski_classes.csv'
categ_df = pd.read_csv(categ)

from twint_ops import twint_query_pars

tw = twint_query_pars()

""" Reading Ukrainian stopwords
"""
stopwords_ua_file = my_dir['data'] + tw['stopwords_ua_file']
stopwords_ua_df = pd.read_csv(stopwords_ua_file, index_col=False, header=None)
stopwords_ua = list(stopwords_ua_df.iloc[:,0])

""" Building ngrams
"""
from nlp_akhmel import ngrams_info

ngrams_info(twits_df['tweet'],n=3,most_common=20,ua_stemmer=True,
            stop_words=stopwords_ua)

""" Classifying
"""
import nltk
from sklearn.model_selection import train_test_split
from nlp_akhmel import ua_tokenizer
    
def bag_of_words(document_tokens,word_features):
        """ Return the dict of bag_of_words. 

        Keyword arguments:
        document_tokens -- list of tokens
        word_features -- list of features
        """
        
        features={}
        for word in word_features:
            features['contains({})'.format(word)]=(word[0] in document_tokens)
        
        return features

def nltk_classifiers(dataframe,X_column,y_column,classifier=nltk.NaiveBayesClassifier,n=1,stop_words=[],ua_stemmer=True,most_common=1000):
    
    words=dataframe[X_column].str.cat(sep=' ')
    words=nltk.ngrams(ua_tokenizer(words,ua_stemmer=ua_stemmer,stop_words=stop_words),n=n)
    words=nltk.FreqDist(words)
    word_features=words.most_common(most_common)
    word_features=[words[0] for words in word_features]
    
    labeled_featuresets=[]
    for _,row in dataframe.iterrows():
        row[X_column]=nltk.ngrams(ua_tokenizer(row[X_column],ua_stemmer=ua_stemmer,stop_words=stop_words),n=n)
        row[X_column]=[words[0] for words in nltk.FreqDist(row[X_column])]        
        labeled_featuresets.append((bag_of_words(row[X_column],word_features=word_features), row[y_column]))  
        
    train_set,test_set,_,_=train_test_split(labeled_featuresets,dataframe[y_column],stratify=dataframe[y_column],test_size=0.33)
    
    if classifier==nltk.MaxentClassifier:
        classifier=classifier.train(train_set, max_iter=5)
    else:
        classifier=classifier.train(train_set)         
    accuracy_train=nltk.classify.accuracy(classifier, train_set)
    accuracy=nltk.classify.accuracy(classifier, test_set)
    print('Точність класифікатора на навчальних даних:',accuracy_train)
    print('Точність класифікатора на тестових даних:',accuracy)
    y_true=[]
    y_pred=[]
    for test in test_set:
        y_true.append(test[1])
        y_pred.append(classifier.classify(test[0]))
    confmat=nltk.ConfusionMatrix(y_pred,y_true)
    print(confmat)
    return classifier   


classifiers = [nltk.NaiveBayesClassifier,nltk.MaxentClassifier,nltk.DecisionTreeClassifier]
for y_column in ('Категорія_Ід2',):
    for classifier in classifiers:    
        for n in (1,2,3):      
            print ('Класифікатор -',classifier)
            print ('Порядок n -',n)           
            print ('Класифікатор за колонкою -',y_column) 
            model = nltk_classifiers(twits_df,X_column='tweet',y_column=y_column,classifier=classifier, n=n, stop_words=stopwords_ua)
            if classifier == nltk.NaiveBayesClassifier:
                print ('Найважливіші токени для класифікації за колонкою -',y_column)
                model.show_most_informative_features(20)