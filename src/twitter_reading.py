#!/usr/bin/env python
# coding: utf-8

# ## Пролог
# 
# Метою цього прикладу є збір твітів з Twitter з використанням API v2 з допомогою Python 3. Це включатиме покроковий процес від налаштування, доступу до кінцевих точок (*End Points*) до збереження твітів, зібраних у форматі CSV.
# 
# Перед запуском прикладу був отриманий доступ Порталу Розробника Твіттера, там створений Проєкт *SCENTSCAPE* і в проєкті створений застосунок *scent_scape_app*. Також в процесі були отримані та збережені ключі доступу застосунку, так звані, *Bearer Token* та *Access Token and Secret*. Ці деталі тут не висвітлені. З огляду на вам потрібно самостійно отримати обліковку на Порталі Розробника Твіттер. Це займе певний час через веріфікацію службою Твіттер наданої вами інформації. Можуть, як у моєму випадку, поставити додаткові питання. Тобто від вимагається чіткість формулювань і певна терплячість.
# 
# Цей приклад побудований на статті [Collecting tweets from Twitter API v2 using Python 3 | Towards Data Science](https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a). У мене немає обліковки API Розробника Тіттер для Академічних досліджень, що дозволяє безкоштовно видобувати 10 млн. твітерів щомісяця. Тому я модифікував код так, щоб отримувати твітери в межах останніх 7 днів. Також у коді виправлена одна явна помилка.

# ## Основні бібліотеки
# 
# Перед початком імпортуємо деякі основні бібліотеки для цього, необхідні для цього прикладу:

# In[24]:


# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For displaying the data after
import pandas as pd
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time
import json


# ## Підготовка авторизації
# 
# Ми досягли цієї точки і, отже, маємо право надіслати свій перший запит з API. По-перше, ми створимо функцію `auth()`, що матиме *Bearer Token* із застосунку, що ми щойно створили. Оскільки цей токен є конфіденційною інформацією, ми не повинні ділитися ним взагалі з ким-небудь. 
# 
# Отже, спочатку збережемо токен в окремому JSON-файлі 'config_auth.json':
# 
# ```json
#   {
#     "token": "<тут-розміщений-ваш-токен>"
#   }
# ```
# 
# Відносний шлях цього файлу включимо до списку `.gitignore`, щоб запобігти його копіюванню на зовнішній ресурс *github*:
# 
# ```
#   src/config_auth.json
# ```
# 
# Після цього прочитаємо наш токен з JSON-файлу:

# In[25]:


config_json = 'config_auth.json'
with open(config_json) as config_json_file:
    config = json.load(config_json_file)

def auth():
    return config['token']

# control display
# auth()


# Далі визначимо функцію, що візьме наш токен, передасть його на авторизацію та поверне заголовки, що ми використовуватимемо для доступу до API.

# In[27]:


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

# control display
#create_headers(auth())


# ## Створюємо URL і параметри запиту для кінцевої точки
# 
# Після отримання доступу до API створимо запит на кінцеву точку, що ми використовуватимемо, та параметри, що ми хочемо передати:

# In[28]:


def create_url(keyword, start_date, end_date, max_results = 10):
    
    search_url = "https://api.twitter.com/2/tweets/search/recent" #Change to the endpoint you want to collect data from

    #change params based on the endpoint you are using
    query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)


# Визначена вище функція складається з двох частин:
# 1. `search_url`: Це посилання кінцевої точки, до якої ми хочемо отримати доступ.
# 2. `query_params`: Параметри, що визначені кінцевою точкою (*end point*), і які можна використовувати для налаштування запиту.

# API твіттера має багато різних кінцевих точок (*end point*). Нижче наданий їхній список, наявний на момент написання цієї статті, де за посиланням можна знайти специфікацію параметрів запиту для кожної кінцевої точки:
# 
# | Категорія      | Кінцева точка                                                | Пояснення                                                    |
# |:--------------|:------------------------------------------------------------|:------------------------------------------------------------|
# | **Tweets**     | [**Tweet lookup**](https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/introduction) | Шукати твіти за Ід.                                          |
# |                | [**Search Tweets**](https://developer.twitter.com/en/docs/twitter-api/tweets/search/introduction) | Запитати останні сім днів або повний архів твітів та отримати<br/>повну відповідь. Повна архівна кінцева точка пошуку<br/>наразі доступна лише у версії продукту *Academic Research*. |
# |                | [**Tweet counts**](https://developer.twitter.com/en/docs/twitter-api/tweets/counts/introduction) | Отримати кількість твітів за останні сім днів або з повного<br/>архіву, що відповідає запиту. Повна архівна кінцева точка підрахунку<br/>твітів наразі доступна лише у версії продукту *Academic Research*. |
# |                | [**Timelines**](https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/introduction) | Отримати хронологію будь-яких твітів, складених з певного облікового<br/>запису Twitter, або згадок про певний обліковий запис Twitter. |
# |                | [**Filtered stream**](https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/introduction) | Відфільтрувати весь потік публічних твітів у реальному часі. |
# |                | [**Sampled stream**](https://developer.twitter.com/en/docs/twitter-api/tweets/sampled-stream/introduction) | Передавати порцію нових твітів по мірі їхньої публікації,<br/>біля ~ 1% усіх публічних твітів у режимі реального часу. |
# |                | **[Retweets](https://developer.twitter.com/en/docs/twitter-api/tweets/retweets/introduction)** | Отримати список облікових записів, які ретвітнули<br/>твіт або ретвіт, або скасували ретвіт твіту. |
# |                | [**Likes**](https://developer.twitter.com/en/docs/twitter-api/tweets/likes/introduction) | Отримати список користувачів, яким сподобався твіт, отримайте список<br/>твітів, що були вподобані або не вподобані користувачем. |
# |                | [**Hide replies**](https://developer.twitter.com/en/docs/twitter-api/tweets/hide-replies/introduction) | Приховати або показати відповідь на твіт.                    |
# | **Users**      | [**User lookup**](https://developer.twitter.com/en/docs/twitter-api/users/lookup/introduction) | Шукати користувачів за іменем або Ід.                        |
# |                | [**Follows**](https://developer.twitter.com/en/docs/twitter-api/users/follows/introduction) | Отримати послідовників облікового запису, отримати список, за ким підписався<br/>обліковий запис, або стежити за користувачем чи припинити слідкувати. |
# |                | [**Blocks**](https://developer.twitter.com/en/docs/twitter-api/users/blocks/introduction) | Отримати список користувачів, яких обліковий запис заблокував,<br/>або заблокувати та розблокувати користувача. |
# |                | **[Mutes](https://developer.twitter.com/en/docs/twitter-api/users/mutes/introduction)** | Вимкнути або увімкнути користувача                           |
# | **Spaces**     | **[Lookup Spaces](https://developer.twitter.com/en/docs/twitter-api/spaces/lookup)** | Пошук простору за допомогою Ід або імені автора              |
# |                | **[Search Spaces](https://developer.twitter.com/en/docs/twitter-api/spaces/search)** | Шукати простори за ключовим словом                           |
# | **Compliance** | **[Batch compliance](https://developer.twitter.com/en/docs/twitter-api/compliance/batch-compliance)** | Пакетне завантаження набору даних, щоб зрозуміти, що потрібно зробити,<br/>щоб ваші набори даних відображали поточний стан вмісту в Twitter. |

# Параметри запиту можна розділити на три групи:
# 
# | Ключове слово<br/>параметра запиту                           | Група параметрів                                             |
# | ------------------------------------------------------------ | ------------------------------------------------------------ |
# | 'query'<br/>'start_time'<br/>'end_time'<br/>'max_results'   | Параметри для контроля повернутого<br/>відгуку на запит          |
# | 'expansions'<br/>'tweet.fields'<br/>'user.fields'<br/>'place.fields' | Додаткові поля, що можна включити<br/>до відгуку на запит       |
# | 'next_token'                                                 | Ункальний ідентифікатор поля для доступу<br/>до наступної сторінки результатів |

# ## Важливі деталі
# 
# Тепер, коли ми знаємо, що робить функція `create_url`, декілька важливих деталей:
# 
# ### Необхідні кінцеві точки:
# 
# У разі повноархівної кінцевої точки пошуку параметр *query* є єдиним параметром, **необхідним** для подання запиту. Завжди переглядайте документацію щодо використовуваної кінцевої точки для належного формування параметрів запиту, щоб уникнути проблем.
# 
# ### Параметр запиту:
# 
# Параметр *query* - це місце, де ви розміщуєте ключові слова, що потрібно шукати.
# 
# Запити можуть бути такими ж простими, як пошук твітів, що містять слово `'xbox'`, або такими складними, як-то `'(xbox europe) OR (xbox usa)'`, що поверне твіти, що містять слова `'xbox AND europe OR xbox AND usa'`.
# 
# Крім того, *query* можна налаштувати з допомогою *операторів пошуку*. Існує так багато варіантів, які допомагають звузити результати пошуку. Повний список цих операторів можна знайти [тут](https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query).
# 
# Приклад простого запиту з оператором: `'xbox lang:en'`.
# 
# ### Мітки часу:
# 
# Формат, що використовує Твіттер для параметрів (міток часу) *end_time* і *start_time*, відповідає стандарту ISO 8601/RFC 3339:
# 
# * `YYYY-MM-DDTHH:mm:ss.fffZ`
# 
# Тому обов’язково перетворіть потрібні дати в цей формат.
# 
# ### Обсяг результатів:
# 
# Кількість результатів пошуку, повернутих за запитом, наразі обмежена від 10 до 500 результатів.
# 
# Тепер з'ясуємо як можна отримати більше 500 результатів? Ось тут гратиме *next_token* та розбивка на сторінки!
# 
# Відповідь проста: якщо на ваш запит повернуто більше результатів, Twitter поверне унікальний *next_token*, що можна використати для наступного запиту і він поверне наступні нові результати.
# 
# Якщо ви хочете отримати всі можливі твіти для вашого запиту, ви просто продовжуєте посилати запити, використовуючи щоразу новий (наступний) *next_token* доти, доки *next_token* не припинить існувати (`None`), сигналізуючи тим самим, що видобуті всі твіти.

# ## Підключення до кінцевої точки
# 
# Тепер, коли у нас є потрібна URL-адреса, заголовки та параметри, ми створимо функцію, що об’єднає все це разом і підключиться до кінцевої точки.
# 
# Нижче наведена функція надішле запит “GET”, і якщо все вірно (код відповіді 200), вона поверне відповідь у форматі “JSON”.
# 
# **Примітка:** за замовчуванням для *next_token* встановлено значення `None`, оскільки нас цікавить результат лише за наявності *next_token.

# In[29]:


def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


# ## Об’єднаємо все разом
# 
# Тепер, коли у нас є всі необхідні функції, давайте спробуємо зібрати їх усі разом, щоб створити наш перший запит!
# У наступній комірці ми налаштуємо наші вхідні дані:
# 
# * *bearer_token* та заголовки з API.
# * Ми будемо шукати твіти англійською мовою, що містять слово “xbox”.
# * Ми будемо шукати твіти в межах останніх 7 днів (стільки дозволяє мій бекоштовний тарифний план). Також обв'язково зазначте мікросекунди в шаблоні часу - інакше Твіттер не пропустить.
# * Ми хочемо повернути максимум 15 твітів.

# In[30]:


#Inputs for the request
bearer_token = auth()
headers = create_headers(bearer_token)
# It looks like geocode does not work in API for the standrad tariff model.
# Though it works in Twitter directly. The issue has to be explored.
keyword = '(воздух OR воздуха)' # +' geocode:50.449949,30.523217,30km'

def twt_datetime_str(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'

end_time = datetime.datetime.now() - datetime.timedelta(hours=4)
start_time = end_time - datetime.timedelta(days=6)
end_time = twt_datetime_str(end_time)
start_time = twt_datetime_str(start_time)

max_results = 15


# In[31]:


url = create_url(keyword, start_time,end_time, max_results)
json_response = connect_to_endpoint(url[0], headers, url[1])
print(json.dumps(json_response, indent=4, sort_keys=True))


# ### Використання отриманих даних
# 
# Отримані дані предствлені списком словників, кожен з яких представляє дані окремого твіту. Нижче наведений приклад отримання часу створення першого твіту:

# In[32]:


json_response['data'][0]['created_at']


# ### Мета дані запиту
# 
# Мета дані запиту представлені словником атрибутів запиту. Зазвичай нас буде цікавити лише про два параметри в цьому словнику, а саме: *next_token* та *result_count*.

# In[33]:


json_response['meta']['result_count']


# In[34]:


json_response['meta']['next_token']


# ## Збереження результатів
# 
# У нас є два варіанти збереження результатів: або зберегаємо результати у тому ж форматі JSON, що ми отримали, або у форматі CSV.
# 
# Зберегти результати в JSON можна легко з допомогою двох рядків коду:

# In[35]:


with open('data_test.json', 'w') as f:
    json.dump(json_response, f)


# ### CSV
# 
# #### Простий підхід
# 
# Простий підхід просто сконструювати з допомогою стандартних бібліотек. Але він не розрахований на вкладені структури словників. Для цього підходу використовуємо пакет *Pandas*:

# In[36]:


df = pd.DataFrame(json_response['data'])
df.to_csv('data_test_simple.csv')


# #### Власний підхід
# 
# Спочатку створимо файл CSV з потрібними заголовками стовпців. Зробимо це окремо від нашої фактичної функції, щоб згодом це не заважало циклічному перегляду запитів.

# In[37]:


# Create file
csvFile = open("data_test_custom.csv", "a", newline="", encoding='utf-8')
csvWriter = csv.writer(csvFile)

#Create headers for the data you want to save, in this example, we only want save these columns in our dataset
csvWriter.writerow(['author id', 'created_at', 'geo', 'id','lang', 'like_count', 'quote_count', 'reply_count','retweet_count','source','tweet'])
csvFile.close()


# Потім створимо нашу основну функцію `append_to_csv`, у яку вхідними аргументами подамо відповідь на запит `json_response` та ім’я файлу `fileName`, а функція додасть усі зібрані нами дані до файлу CSV.

# In[38]:


def append_to_csv(json_response, fileName):

    #A counter variable
    counter = 0

    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Loop through each tweet
    for tweet in json_response['data']:
        
        # We will create a variable for each since some of the keys might not exist for some tweets
        # So we will account for that

        # 1. Author ID
        author_id = tweet['author_id']

        # 2. Time created
        created_at = dateutil.parser.parse(tweet['created_at'])

        # 3. Geolocation
        if ('geo' in tweet):   
            geo = tweet['geo']['place_id']
        else:
            geo = " "

        # 4. Tweet ID
        tweet_id = tweet['id']

        # 5. Language
        lang = tweet['lang']

        # 6. Tweet metrics
        retweet_count = tweet['public_metrics']['retweet_count']
        reply_count = tweet['public_metrics']['reply_count']
        like_count = tweet['public_metrics']['like_count']
        quote_count = tweet['public_metrics']['quote_count']

        # 7. source
        source = tweet['source']

        # 8. Tweet text
        text = tweet['text']
        
        # Assemble all data in a list
        res = [author_id, created_at, geo, tweet_id, lang, like_count, quote_count, reply_count, retweet_count, source, text]
        
        # Append the result to the CSV file
        csvWriter.writerow(res)
        counter += 1

    # When done, close the CSV file
    csvFile.close()

    # Print the number of tweets for this iteration
    print("# of Tweets added from this response: ", counter) 


# Тепер, коли ми запустимо нашу функцію `append_to_csv()`, ми маємо отримати файл, що містить 15 твітів (або менше, залежно від результату запиту)

# In[39]:


append_to_csv(json_response, "data_test_custom.csv")


# Отже, ми можемо встановити обмеження на кількість твітів, що ми збираємо за певний період часу, так що, якщо ми досягнемо певного (встановленого нами) обмеження за цей період, ми перейдемо до наступного.
# 
# Код нижче - це приклад, що точно зробить це! Цей блок коду складається з двох циклів:
# 
# 1. Цикл `for`, що перебирає ці періоди часу (залежно від того, як це налаштовано)
# 2. Цикл `While`, що контролює максимальну кількість твітів, що ми хочемо зібрати за певний період часу.
# 
# Зверніть увагу, що між викликами додається `time.sleep()`, щоб переконатися, що ви не просто спасимите API через запити.

# In[40]:


# Inputs for tweets
bearer_token = auth()
headers = create_headers(bearer_token)
# The query 'keyword' is defined above
#keyword = 'geocode:50.449949,30.523217,30km (воздух OR воздуха)'

end_time = datetime.datetime.now() - datetime.timedelta(hours=4)
time_list = [end_time - datetime.timedelta(days=x) for x in [6,4,2,0]]
start_list = [twt_datetime_str(time_list[i]) for i in range(3)]
end_list = [twt_datetime_str(time_list[i]) for i in range(1,4)]

max_results = 50

#Total number of tweets we collected from the loop
total_tweets = 0

# Create file
data_complete_file = "data_complete.csv"
csvFile = open(data_complete_file, "a", newline="", encoding='utf-8')
csvWriter = csv.writer(csvFile)

#Create headers for the data you want to save, in this example, we only want save these columns in our dataset
csvWriter.writerow(['author id', 'created_at', 'geo', 'id','lang', 'like_count', 'quote_count', 'reply_count','retweet_count','source','tweet'])
csvFile.close()

for i in range(0,len(start_list)):

    # Inputs
    count = 0 # Counting tweets per time period
    max_count = 100 # Max tweets per time period
    flag = True
    next_token = None
    
    # Check if flag is true
    while flag:
        # Check if max_count reached
        if count >= max_count:
            break
        print("-------------------")
        print("Token: ", next_token)
        url = create_url(keyword, start_list[i],end_list[i], max_results)
        json_response = connect_to_endpoint(url[0], headers, url[1], next_token)
        result_count = json_response['meta']['result_count']

        if 'next_token' in json_response['meta']:
            # Save the token to use for next call
            next_token = json_response['meta']['next_token']
            print("Next Token: ", next_token)
            if result_count is not None and result_count > 0 and next_token is not None:
                print("Start Date: ", start_list[i])
                append_to_csv(json_response, data_complete_file)
                count += result_count
                total_tweets += result_count
                print("Total # of Tweets added: ", total_tweets)
                print("-------------------")
                time.sleep(5)                
        # If no next token exists
        else:
            if result_count is not None and result_count > 0:
                print("-------------------")
                print("Start Date: ", start_list[i])
                append_to_csv(json_response, data_complete_file)
                count += result_count
                total_tweets += result_count
                print("Total # of Tweets added: ", total_tweets)
                print("-------------------")
                time.sleep(5)
            
            #Since this is the final request, turn flag to false to move to the next time period.
            flag = False
            next_token = None
        time.sleep(5)
print("Total number of results: ", total_tweets)


# Перевірте ваш робочий фолдер — там з’явились 4 згенерованих файли: 
# 
# - `data_test.json`
# - `data_test_simple.csv`
# - `data_test_custom.csv`
# - `data_complete.csv`
# 
# Якщо так, то вітаю вас — все працює!
