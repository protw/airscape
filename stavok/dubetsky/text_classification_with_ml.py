# -*- coding: utf-8 -*-
"""Text Classification with ML-Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jN6p8BiYLHD5qnUKHIhRDPBTp6pAxLhm
"""

data_ind = 1 # 0 - Dubetsky, 1 - Bond
data_src = ['Dubetsky', 'Bond'][data_ind]
if data_src == 'Dubetsky': # Oleg Dubetsky data
    csv_file = 'https://raw.githubusercontent.com/olegdubetcky/Text-Classification-with-ML-Project/main/news.csv'
elif data_src == 'Bond':   # Olegh Bond data
    csv_file = 'https://raw.githubusercontent.com/protw/airscape/master/src/data/twint_zelenski_categ.csv'

import pandas as pd
df = pd.read_csv(csv_file, encoding='utf8')

import sys
sys.path.append('../../')
from twint_ops import twint_query_pars, set_path_pre
from nlp_akhmel import ua_tokenizer
import simplemma as sl

def create_corpus(df):
    ## Fetch ukr stopwords
    tw = twint_query_pars()
    stopwords_ua_file = tw['stopwords_ua_file']
    stopwords_ua_file = set_path_pre(stopwords_ua_file)
    stopwords_ua_df = pd.read_csv(stopwords_ua_file, index_col=False, 
                                  header=None)
    stopwords_ua = list(stopwords_ua_df.iloc[:,0])
    ## Rename columns according to Dubetsky
    df.rename(columns={'tweet':'title','Категорія':'category'},
              inplace=True)
    ## Clean, remove stopwords, tokenize and create text corpus (list of lists)
    corpus = df['title'].apply(lambda x : ua_tokenizer(x,ua_stemmer=False,
                                          stop_words=stopwords_ua)).tolist()
    ## Lematizing text corpus
    langdata = sl.load_data('uk')
    new_corp = []
    for tok_list in corpus:
        lem_list = [sl.lemmatize(t, langdata) for t in tok_list]
        new_corp.append(' '.join(lem_list))
    return new_corp

if data_src == 'Bond':
    corpus = create_corpus(df)

elif data_src == 'Dubetsky':
    #перетворіть усі дані у нижній регістр, а потім збережіть їх у форматі списку
    corpus = df['title'].apply(lambda x : str(x).lower()).tolist()

df.category.unique()


#встановити цільові змінні
y = df['category']

import pickle
from sklearn.feature_extraction.text import CountVectorizer

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(corpus)

#зберегти ветори слів 
pickle.dump(count_vect.vocabulary_, open("feature.pkl","wb"))

from sklearn.feature_extraction.text import TfidfTransformer

#перетворення векторів слів до TF IDF
tfidf_transformer = TfidfTransformer()
X = tfidf_transformer.fit_transform(X_train_counts)

#зберегти TF-IDF
pickle.dump(tfidf_transformer, open("tfidf.pkl","wb"))

#розділити дані на зразки для навчання та тестування
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Multinomial Naive Bayes
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train, y_train)

#SAVE MODEL
pickle.dump(clf, open("nb_model.pkl", "wb"))

from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn import metrics


#проста функція оцінки
def evaluate(clf, X_train = X_train, X_test = X_test, y_train = y_train, y_test = y_test):
    
    import seaborn as sns
    
    print('Класифікатор : {}'.format(clf))
    clf.fit(X_train, y_train)
    # Predict Test Data 
    y_pred = clf.predict(X_test)

    # Calculate accuracy, precision, recall, f1-score, and kappa score
    acc = metrics.accuracy_score(y_test, y_pred)
    prc = metrics.precision_score(y_test, y_pred, average='macro')
    rec = metrics.recall_score(y_test, y_pred, average='macro')
    f1 = metrics.f1_score(y_test, y_pred, average='macro')
    kappa = metrics.cohen_kappa_score(y_test, y_pred)

   
    # Display confussion matrix
    cm = metrics.confusion_matrix(y_test, y_pred)
    
    print('Метрики : \n')
   # Print result
    print('Точність:', acc)
    print('Влучність:', prc)
    print('Повнота:', rec)
    print('F1 міра:', f1)
    print('Cohens Kappa міра:', kappa)
    print('Матриця невідповідностей:\n', cm)
    
    print('*'*100)
    print('\n\n')
    
    return {'acc': acc, 'prc': prc, 'rec': rec, 'f1': f1, 'kappa': kappa, 'cm': cm}


#ініціалізувати класифікатори
mnb = MultinomialNB()
mlp_neural = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)
svm = SVC(decision_function_shape='ovo') #one vs one strategy
lin_svm = LinearSVC()
dt = DecisionTreeClassifier()
rf = RandomForestClassifier(n_estimators = 150)

#викликати функцію оцінки, яку ми створили для класифікаторів
evaluate(mnb)


mlp_neural_eval = evaluate(mlp_neural)
svm_eval = evaluate(svm)
lin_svm_eval = evaluate(lin_svm)
dt_eval = evaluate(dt)
rf_eval = evaluate(rf)

import matplotlib.pyplot as plt
import numpy as np
# Intitialize figure with two plots
fig, (ax1) = plt.subplots(1)
fig.suptitle('Порівняння моделей', fontsize=16, fontweight='bold')
fig.set_figheight(7)
fig.set_figwidth(16)
fig.set_facecolor('white')

## set bar size
barWidth = 0.2

mlp_neural_eval_score = [mlp_neural_eval['acc'], mlp_neural_eval['prc'], mlp_neural_eval['rec'], mlp_neural_eval['f1'], mlp_neural_eval['kappa']]
svm_score = [svm_eval['acc'], svm_eval['prc'], svm_eval['rec'], svm_eval['f1'], svm_eval['kappa']]
lin_svm_score = [lin_svm_eval['acc'], lin_svm_eval['prc'], lin_svm_eval['rec'], lin_svm_eval['f1'], lin_svm_eval['kappa']]
dt_score = [dt_eval['acc'], dt_eval['prc'], dt_eval['rec'], dt_eval['f1'], dt_eval['kappa']]
rf_score = [rf_eval['acc'], rf_eval['prc'], rf_eval['rec'], rf_eval['f1'], rf_eval['kappa']]

## Set position of bar on X axis
r1 = np.arange(len(mlp_neural_eval_score))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
r4 = [x + barWidth for x in r3]
r5 = [x + barWidth for x in r4]

## Make the plot
ax1.bar(r1, mlp_neural_eval_score, width=barWidth, edgecolor='white', label='MultinomialNB')
ax1.bar(r2, svm_score, width=barWidth, edgecolor='white', label='SVC')
ax1.bar(r3, lin_svm_score, width=barWidth, edgecolor='white', label='LinearSVC')
ax1.bar(r4, dt_score, width=barWidth, edgecolor='white', label='DecisionTree')
ax1.bar(r5, rf_score, width=barWidth, edgecolor='white', label='RandomForest')
plt.legend()
## Configure x and y axis
ax1.set_xlabel('Метрики', fontweight='bold')
labels = ['Точність', 'Влучність', 'Повнота', 'F1', 'Kappa']
ax1.set_xticks([r + (barWidth * 1.0) for r in range(len(mlp_neural_eval_score))], )
ax1.set_xticklabels(labels)
ax1.set_ylabel('Оцінка', fontweight='bold')
ax1.set_ylim(0, 1)

from sklearn.model_selection import GridSearchCV
#спробуйте налаштувати параметри. Для LinearSVC C є регульованим параметром
params = {'C': [0.1, 1, 10, 100, 1000]}
#використовувати клас GridSearchCV. Основними аргументами є (класифікатор, параметри), для яких ми хочемо виконати найкращий пошук параметрів.
grid = GridSearchCV(LinearSVC(), params, refit=True, verbose=3)
#пристосувати дані навчання до нашої моделі grid_search та перевірити прогнози на нашому тестовому наборі
grid.fit(X_train, y_train)
y_pred = grid.predict(X_test)
#Перевірте точність і влучність нашої моделі
print('Точність : {:.2f}%'.format(100*metrics.accuracy_score(y_pred, y_test)))
print('Влучність : \n{}'.format(100*metrics.precision_score(y_pred, y_test, average = None)))

import pickle

#зберегти модель категорії

pickle.dump(grid, open('LinearSVM_model.pkl', 'wb'))

# завнтажити модель категорії та перевірити
tuned_model = pickle.load(open('LinearSVM_model.pkl', 'rb'))
result = tuned_model.score(X_test, y_test)*100

print('Точність : {:.2f}%'.format(result)) 

loaded_vec = CountVectorizer(vocabulary=pickle.load(open("feature.pkl", "rb")))
loaded_tfidf = pickle.load(open("tfidf.pkl","rb"))
loaded_model = pickle.load(open("LinearSVM_model.pkl","rb"))

docs_news = {
    'tweet':["У телефонній розмові @sandumaiamd подякувала Україні за швидку допомогу під час енергетичної кризи. Запевнив у готовності Прапор України й надалі допомагати Прапор Молдови у питанні постачання газу. Обговорили реалізацію проекту будівництва мосту через Дністер і підготовку до саміту",
             "Вітаю мого друга @RTErdogan і весь турецький народ з 98-ю річницею проголошення Турецької Республіки. Високо ціную стратегічне партнерство наших держав. Переконаний, що відносини між Прапор України й Прапор Туреччини мають великий потенціал для розвитку. Бажаю миру та процвітання Прапор Туреччини"
            ],
    'Категорія': ['qwert','qwert']
    }
corp_test = create_corpus(pd.DataFrame.from_dict(docs_news))
for docs_new in corp_test:
    X_new_counts = loaded_vec.transform([docs_new])
    X_new_tfidf = loaded_tfidf.transform(X_new_counts)
    predicted = loaded_model.predict(X_new_tfidf)
    print('Категорія: ', predicted[0])