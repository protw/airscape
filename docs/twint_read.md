# Зчитування твітів з допомогою *Twint*

## Вступ

[Twint](https://github.com/twintproject/twint) - це вдосконалений інструмент для збирання твітів (скорочення від *Twitter Intelligence Tool*). Цей пакет побудований на *Python* і збирає дані твітів з веб-сторінки (так званий *scraping*) замість того, щоб збирати їх через *API Twitter*, як-от це робить *tweepy*.

## Середовище

Для початку рекомендовано організувати окреме середовище для роботи, налаштувань і залежностей (*dependencies*). Для цього ви маєте ознайомитись з інструментом [Anaconda](https://www.anaconda.com/).

Після встановлення *Anaconda* створімо окреме середовище *twitter* для збирання і обробки твітів:

```bash
conda create --name twitter python=3.9
```

Одразу активуємо середовище *twitter*:

```bash
conda activate twitter
```

А також встановимо інструмент для роботи з кодом *spyder* або, як у нашому випадку, *jupyter notebook*:

```bash
conda install -c conda-forge jupyterlab
```

## Встановлення *twint*

Деякі публікації замість встановлення *twint* з допомогою стандартного інструменту керування пакетами в *python* - *pip* рекомендують натомість встановлення безпосередньо з *git* репозитарія:

```bash
git clone https://github.com/twintproject/twint.git
cd twint
pip3 install . -r requirements.txt
```

## Почнімо

Окрім програмного API (*Application Programming Interface*) *twint* має дуже розлогий [інтерфейс командного рядка](https://github.com/twintproject/twint/wiki/Basic-usage).

Отже спробуємо зібрати твіти відомої публічної особи, наприклад, Президента України пана Зеленського [@ZelenskyyUa](https://twitter.com/ZelenskyyUa).

Для цього підготуємо параметри запиту:

```python
#### SET TWINT QUERY PARAMETERS

def twint_query_pars():
    tw = {}
    tw['user'] = 'ZelenskyyUa'
    tw['output_type'] = 'csv'
    tw['output_name'] = 'twint_zelenski.csv'
    tw['since'] = '2019-04-01'
    return tw

tw = twint_query_pars()
```

## Запит з командного рядка

Спочатку зчитаємо твіти цього користувача скориставшись інтерфейсом командного рядка. Перед запуском розкоментуйте останній рядок у фрагменті коду нижче.

```python
#### RUN QUERY VIA CLI

import os

def twint_cli(tw):

    #!twint -u ZelenskyyUa --since 2019-04-01 -o twint_zelenski.csv --csv
    tw_run_str = 'twint' + \
                 ' -u '  + tw['user'] + \
                 ' --'   + tw['output_type'] + \
                 ' -o '  + tw['output_name']
    return tw_run_str

tw_run_str = twint_cli(tw)
#os.system(tw_run_str) # uncomment if necessary
```

## Запит через API

Тепер проведемо той же запит через API. Перед запуском розкоментуйте останній рядок у фрагменті коду нижче.

```python
#### RUN QUERY VIA API

import twint
import nest_asyncio
nest_asyncio.apply()

def twint_api(tw):
    c = twint.Config()

    c.Username = tw['user']
    c.Store_csv = (tw['output_type'] == 'csv')
    c.Output = tw['output_name']

    twint.run.Search(c)

    tweets = twint.output.tweets_list
    len(tweets)
    return

#twint_api() # uncomment if necessary
```

## Щось пішло не так

Щось пішло не так - всього отримав 7 твітів. Це явно і набагато менше, ніж можна побачити на Твіттері. Варіації параметрів, запуск з командного рядка не дали змін.

Занурення у форуми через пошук за запитом `[!] No more data! Scraping will stop now. found 0 deleted tweets in this search.` вивели на [таке рішення](https://github.com/twintproject/twint/issues/1253#issuecomment-913055717), в якому рекомендовано найти в коді встановленого пакету *twint* файл *url.py* і зняти коментар (#) з 92 рядка, що має такий вигляд:

```python
# ('query_source', 'typed_query'),
```

Для початку довелось пошукати повний шлях до розташування пакету *twint* і файлу *url.py* в ньому. Для Windows 10 цей шлях виявився таким:

```bash
C:\Users\<my_winows_user_name>\miniconda3\envs\airscape\Lib\site-packages\twint\
```

У цьому шляху токен `<my_winows_user_name>` означає ваше користувацьке ім'я в операційній системі Windows 10 на вашому комп'ютері. І дійсно у цьому файлі у зазначеному рядку розташований саме цей фрагмент коду. Розкоментуємо і подивимось.

Вуаля! Десь за пів хвилини отримано 1357 твітів за період з 25.04.2019 до 07.10.2021! Саме квітень 2019 року зазначено як місяць реєстрації цієї обліковки у Твіттері.

## Перегляд зібраних даних

Прочитаємо зібрані дані та заодно видалимо порожні колонки:

```python
#### TWINT QUERY RESULT PROCESSING

import pandas as pd

twint_df = pd.read_csv(tw['output_name'], sep='\t')

def del_empty_columns(df):
    df_desc = df.describe().transpose()
    cols_del = df_desc.index.values[df_desc['count'] == 0]
    return df.drop(columns=cols_del, inplace=False)

twint_df = del_empty_columns(twint_df)
```

## PS. Ще помилки коду

Згодом виявилось, що не працює параметр `c.Lang` в коді - на виході не відбувається фільтрація твітів за мовою (див. [тут](https://github.com/twintproject/twint/pull/1025))

```python
c.Lang = 'uk' # does not work
```

Для виправлення помилки потрібно вставити у файл *url.py* після рядка 113 наступний код:

```python
if config.Lang:
    q += f" lang:{config.Lang}"
```

