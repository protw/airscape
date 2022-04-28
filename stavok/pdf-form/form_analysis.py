import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
from datetime import datetime
from wordcloud import WordCloud
import numpy as np

folder = 'D:/boa_uniteam/UNITEAM/_DOCS/STAFF/ПЕРСОНАЛІЇ/'
form_series = 'АНКЕТА НЕЦУ - 2022'
folder_img = folder + form_series + '/img/'

print(f'FORM_ANALYSIS "{folder + form_series}"')

def get_data():
    data_file = folder + form_series + '.csv'
    data_struct = folder + form_series + ' - Структура.xlsx'
    data_priority = folder + form_series + ' - Пріоритети.xlsx'

    df_data = pd.read_csv(data_file)
    df_struct = pd.read_excel(data_struct)
    df_priority = pd.read_excel(data_priority)

    return df_data, df_struct, df_priority

df_data, df_struct, df_priority = get_data()
print('-- Get data')


def correct_bool_fields(df_data, df_struct):
    
    bool_field = df_struct.loc[df_struct.type == 'bool',['field']]

    '''
    PDF форма у чек-боксі повертає '0.0', або інші небулеві результати, коли є 
    відмітка (тобто значення чек боксу True), і 'nan', коли немає (False). 
    Також трапилась одна форма, де замість 'nan' було повернуто 'Off'.

    Тому робимо такі заміни:
        'Off' -> False
        nan -> False
        type(x) is not bool -> x = True
    '''
    for bf in bool_field['field']:
        df_data[bf] = [False if x == 'Off' else x for x in df_data[bf]]
        df_data[bf] = [False if pd.isnull(x) else x for x in df_data[bf]]
        df_data[bf] = [True if type(x) is not bool else x for x in df_data[bf]]
    
    return df_data

df_data = correct_bool_fields(df_data, df_struct)
print('-- Correct "Bool" fields')

'''
Що будуємо:
    + Розподіл поданих анкет по відокремлених підрозділах (field.pidrozdil)
    + Розподіл використання месенджерів (group.Messenger)
    + Розподіл практичного досвіду (field.vnz_rik)
    + Розподіл комп'ютерних навичок (group.ICT)
    + Розподіл управлінських навичок (group.Management)
    + Розподіл тривалості досвіду (2022 - field.vnz_rik)
    + Кількість людей: без вищої освіти, з вищою освітою (field.vnz_rik), 
                       кандидатів, докторів (field.nauk_stupinj)
    - Лінгвістичний аналіз 
         - Чим ви хотіли б займатися в НЕЦУ (field.necu_intention)
         - Ваш досвід роботи в екологічному русі (field.eco_experience)
         - Пріоритетні напрями діяльності НЕЦУ (field.necu_priorities)
'''

'''
Побудова гістограми з таблиці логічних даних. Таблиця формується зі стовпців
'df_data', що належать до групи 'group'. По кожному стовпчику підраховується
кількість значень 'True'. Тобто в підсумку маємо таблицю 'df_hist' з двома 
стовпчиками: 'item' - категорія, що відповідає назві стовпчика з 'df_data', і
'count' - кількість значень 'True' у цьому стовпчику. Стовпчик 'item' у 
'df_hist' встановлюється індексом.
'''
def hist_by_group(group):
    df_hist = pd.DataFrame({'item':[],'count':[]})
    for f in df_struct.loc[df_struct['group']==group,'field']:
        m = list(df_struct.loc[df_struct['field']==f,'assignment'])[0]
        df_hist = df_hist.append({'item':m, 'count': df_data[f].sum()},
                                 ignore_index=True)

    df_hist.sort_values(by='count',inplace=True)
    df_hist.set_index('item',inplace=True)
    
    return df_hist

''' 
Побудова простої горизонтальної гістограми. Елемент словника "par['hist_data']"
містить об'єкт типу DataFrame або Series, де зберігається гістограма. Індекс 
цього об'єкту містить назви категорій, для яких побудована гістограма.
'''
def plot_barh(par):
    plt.figure()
    par['hist_data'].plot(kind='barh', grid=True)
    plt.xlabel(par['xlabel'])
    plt.ylabel(par['ylabel'])
    plt.title(par['title'])

    img_name = par['img_name'] if 'img_name' in par.keys() else par['title']
    img_name = folder_img + img_name + '.png'
    plt.savefig(img_name, bbox_inches='tight',dpi=150)

# Розподіл поданих анкет по відокремлених підрозділах
plot_barh({
    'hist_data': df_data['pidrozdil'].value_counts(), 
    'xlabel': 'Чисельність членів',
    'ylabel': 'Відокремлений підрозділ',
    'title': 'Подано анкет - ' + str(df_data.shape[0]),
    'img_name': 'Розподіл поданих анкет'
})
print('-- Members by branches')

# Розподіл використання месенджерів
plot_barh({
    'hist_data': hist_by_group(group='Messenger'),
    'xlabel': 'Чисельність членів',
    'ylabel': 'Месенджер',
    'title': 'Використання месенджерів'
})
print('-- Communications')

# Розподіл робочого стажу (cur_year - field.vnz_rik)
def plot_pract():
    cur_year = date.today().year
    data = -(df_data[['vnz_rik']].dropna() - cur_year)
    pract_mean = -(df_data[['vnz_rik']].mean()[0] - cur_year)
    img_name = folder_img + 'Розподіл робочого стажу' + '.png'
    
    plt.figure()
    data.hist()
    plt.xlabel('Робочий стаж, рік')
    plt.ylabel('Кількість членів')
    plt.title(f'Середній стаж = {pract_mean:.1f}')
    plt.savefig(img_name, bbox_inches='tight',dpi=150)

plot_pract()
print('-- Working experience')

# Розподіл комп'ютерних навичок
plot_barh({
    'hist_data': hist_by_group(group='ICT'), 
    'xlabel': 'Чисельність членів',
    'ylabel': 'Навички',
    'title': 'Розподіл комп\'ютерних навичок'
})
print('-- Computer skills')

# Розподіл управлінських навичок
plot_barh({
    'hist_data': hist_by_group(group='Management'), 
    'xlabel': 'Чисельність членів',
    'ylabel': 'Навички',
    'title': 'Розподіл управлінських навичок'
})
print('-- Managerial skills')

def print_stats():
    # Підрахунок осіб зі ступенем кандидата або доктора, окремо
    def degree_count(degree_1st_letter):
        num_of_ = 0
        for s in df_data['nauk_stupinj']:
            if (type(s) is str) and s.lower().startswith(degree_1st_letter):
                num_of_ += 1
        return num_of_
    
    stats = [
        ['Станом на', datetime.now().strftime("%d.%m.%Y %H:%M")], 
        ['Число поданих анкет', str(df_data.shape[0])],
        ['З кількості підрозділів', str(df_data['pidrozdil'].unique().shape[0])],
        ['З них з вищою освітою', str((~df_data['vnz'].isna()).sum())], 
        ['кандидатів наук', str(degree_count('к'))], 
        ['докторів наук', str(degree_count('д'))] 
    ]

    fig, ax = plt.subplots()
    ax.set_axis_off()

    ax.table(cellText=stats, colLoc='left', loc='center')
    
    img_name = folder_img + 'Стат дані' + '.png'
    plt.savefig(img_name, bbox_inches='tight',dpi=150)
   
print_stats()
print('-- General stats')

# Розподіл пріоритетів
plot_barh({
    'hist_data': df_priority['category'].value_counts(), 
    'xlabel': 'Кількість голосів',
    'ylabel': 'Пріоритет',
    'title': 'Рейтинг пріоритетів'
})
print('-- Priority rating')

def priority_wordcloud():
    def prior_dict():
        x = df_priority['category'].value_counts()
        x = dict(list(zip(x.index,x)))
        return dict(sorted(x.items(), key=lambda x: x[1], reverse=True))

    prior_freq = prior_dict()

    del prior_freq['окремі напрями']
    del prior_freq['фітосередовище']

    x = df_priority[df_priority['category']=='окремі напрями']['necu_priorities']
    for y in x:
        prior_freq[y] = 1
    x = df_priority[df_priority['category']=='фітосередовище']['necu_priorities']
    for y in x:
        prior_freq[y] = 1
    
    def set_mask(sz=800):
        x, y = np.ogrid[:sz, :sz]
        mask = (x - sz/2) ** 2 + (y - sz/2) ** 2 > 400 ** 2
        mask = 255 * mask.astype(int)
        return mask

    wrdcld = WordCloud(width=1200, height=800, background_color='white', \
                       mask=set_mask()) \
                       .generate_from_frequencies(prior_freq) \
                       .to_file(folder_img + 'word_freq.png')

    width = 12
    height = 8
    plt.figure(figsize=(width, height))
    plt.imshow(wrdcld)
    plt.axis("off")
    plt.title('Хмара пріоритетів')
    plt.show()

priority_wordcloud()
print('-- Priority wordcloud')

print('DONE!')