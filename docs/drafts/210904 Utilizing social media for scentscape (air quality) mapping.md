# Utilizing social media for scentscape (air quality) mapping

## Task formulation and components needed

The components below are collated in order of their use in technology chain:

1. Collecting the social media data (posts) by certain criteria, first of all, geotag (certain area, city), time period, key words presence, other
2. Analysis of the collected social media data (possibly using NLP) in order to get factor (agent) + emotion

The components next after might not be necessary:

3. NN learning by juxtaposing the factor + emotion versa the concentration of PM and gases + meteo data (temperature, humidity, wind speed, pressure)
4. Factor prediction|monitoring using taught NN

## Два типи скрейпінгу

Треба розрізняти два типи скрейпінгу (це стосується будь-якої соц. мережі): 

1. без API та 
2. з допомогою API

У першому випадку скрейпінг відбувається шляхом зчитування і розбірки (parsing) інформації безпосереднь зі сторінки, відображеній на стороні клєнта. У другому випадку скрейпінг здійснюється із серверних ресурсів соц. мережі з допомогою API. Методи принципово нетотожні, кожний має власні зручності, переваги і обмеження. 

## References

* [Данило Кінь про розпізнавання запахів, ФБ](https://www.facebook.com/100002626391429/posts/4242371732526998/)
* [Перші кроки в NLP: розглядаємо Python-бібліотеку NLTK в реальному завданні | DOU](https://dou.ua/lenta/articles/first-steps-in-nlp-nltk/)
* [NLTK Book](https://www.nltk.org/book/)
* [Top 7 Python NLP Libraries [And Their Applications in 2021] | upGrad blog](https://www.upgrad.com/blog/python-nlp-libraries-and-applications/)
* [GitHub - curiousest/predict-AQI: Predicting air pollution (machine learning project)](https://github.com/curiousest/predict-AQI)
* [The Emotional and Chromatic Layers of Urban Smells](https://arxiv.org/pdf/1605.06721.pdf)
* [Sensory Maps](https://sensorymaps.com/)

## Facebook scrapers

Збирання інфи з ФБ з огляду на драконівські обмеження, введені після скандалу з Кебрідж Аналітика, невдячна справа. Тим не менш, це можливо. 

* [GitHub - kevinzg/facebook-scraper: Scrape Facebook public pages without an API key](https://github.com/kevinzg/facebook-scraper)
* [Facebook Scraper 2021 | How to Scrape Data from Facebook | Best Proxy Reviews](https://www.bestproxyreviews.com/facebook-scraper/)
* [How to Scrape a Medium Publication: A Python Tutorial for Beginners | Hacker Noon](https://hackernoon.com/how-to-scrape-a-medium-publication-a-python-tutorial-for-beginners-o8u3t69)
* [Facebook Graph API | Python. Ever since I was apprised of Python and… | by Shivam Dutt Sharma | Analytics Vidhya | Medium](https://medium.com/analytics-vidhya/facebook-graph-api-python-3c8bab8a5a2a)
* [How to use Facebook Graph API and extract data using Python! | by Ravi Ranjan | Towards Data Science](https://towardsdatascience.com/how-to-use-facebook-graph-api-and-extract-data-using-python-1839e19d6999)

## Twitter Scrapers

Маючи близько 500 мільйонів твітів на день, Twitter - це море інформації, що можна використовувати як чудове джерело для моніторингу бренду та вимірювання настроїв клієнтів. [За даними Громадського](https://hromadske.ua/posts/socmerezhi-2021-tiktok-starshaye-facebook-perevazhno-zhinochij-a-strichku-mi-gortayemo-400-miljoniv-rokiv) в Україні станом на січень 2021 Твіттер охоплює 6% населення проти 59% Фейсбука. Але **на відміну від Facebook, Twitter дозволяє** людям отримувати широкомасштабні дані за допомогою [API Twitter](https://help.twitter.com/en/rules-and-policies/twitter-api).

* [GitHub - bisguzar/twitter-scraper: Scrape the Twitter Frontend API without authentication.](https://github.com/bisguzar/twitter-scraper)
* [Scraping Data Off Twitter Using Python | Twitterscraper + NLP + Data Visualization - YouTube](https://www.youtube.com/watch?v=MpIi4HtCiVk)
   * [GitHub - AlexTheAnalyst/PythonCode](https://github.com/AlexTheAnalyst/PythonCode)
* [Effects of Actual and Perceived Air Pollution on U.S. Twitter Sentiment](https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=1181&context=studentpub_uht)

