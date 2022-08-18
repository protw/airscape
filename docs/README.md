# AirScape

<!-- tabs:start -->

# **Концепт проєкту**

## Проблема

Невпинні кліматичні зміни і збільшення населення міст є основними факторами погіршення якості повітря. Традиційними методами моніторингу якості повітря є розгортання інструментальних мереж моніторингу.

Хоча інструментальні методи моніторингу якості повітря демонструють свою високу ефективність, в умовах сучасних викликів виникають певні проблеми, подолання яких утруднено в рамках традиційних підходів:

1. практично неможливо забезпечити необхідну (бажану, достатню) просторову щільність датчиків;
2. переважна частина датчиків здатні вимірювати досить обмежений перелік фізичних факторів, що визначають якість повітря, тому отриманий ними показник AQI дуже часто буває неповним і, отже, неадекватним;
3. подолання проблем, наведених у пунктах 1 та 2, вимагає розгортання додаткової інфраструктури та її обслуговування, а отже, значних ресурсів.

## Ідея

Масштаб людської активності в глобальній мережі вражає, зокрема:

- 4.8 мільярдів людей по всьому світі скористалось Інтернетом у липні 2021 року - це майже 61% усього населення світу (за даними [Datareportal](https://datareportal.com/global-digital-overview)).
- Станом на березень 2021 року щоденні активні користувачі *Facebook* (DAU) становили 1.88 мільярда (згідно [Facebook Reports First Quarter 2021 Results](https://investor.fb.com/investor-news/press-release-details/2021/Facebook-Reports-First-Quarter-2021-Results/default.aspx)).

- У середньому щодня надсилається 500 мільйонів твітів (за даними [Twitter by the Numbers (2021): Статистика, демографія та цікаві факти](https://www.omnicoreagency.com/twitter-statistics/)).

Враховуючи, що навіть якщо невеликий відсоток цих даних присвячений питанням поточного стану довкілля, то аналізуючи ці дані, можна отримати величезне допоміжне джерело інформації, що може значно розширити можливості інструментальних методів.

?> Основна ідея проекту ***AirScape*** полягає в розширенні інструментальних мереж моніторингу якості повітря альтернативними засобами на основі аналізу даних соціальних медіа (SMD - *social media data*) з використанням геолокалізації, класифікації тексту, аналізу настроїв, та інших методів обробки природної мови (NLP - *natural language processing*), машинного навчання (ML - *machine learning*) та інших методів.

## Переваги

Головною перевагою запропонованого підходу є:

1. набагато ширше та щільніше просторове охоплення з можливостями швидшого відгуку на критичні зміни;
2. ширший перелік можливих оцінюваних фізичних факторів, що впливають на якість повітря, а також на стан довкілля в цілому;
3. немає необхідності розгортати додаткову інструментальну інфраструктуру на місцях.

Таким чином, проект можна розглядати як техніко-економічне обґрунтування розширення інструментальних систем моніторингу якості повітря нетрадиційними методами.

## План

Загальний орієнтовний план розробки передбачає побудову наступного технологічного ланцюга:

1. Збір SMD (постів, твітів) за певними критеріями, насамперед, геоприв'язкою (певна область, місто, район міста), періодом часу, наявністю ключових слів тощо.
2. Аналіз зібраних SMD (можливо, з допомогою NLP) для отримання формуючих факторів та емоцій, що виникають у результаті реакції людини на стан довкілля.
3. Результати аналізу SMD будуть зіставлені з результатами відповідних інструментальних вимірювань і оцінок якості повітря засобами ML, з метою подальшого незалежного використання результатів аналізу SMD особливо там, коли і де результати інструментальних методів відсутні. Тож результати можна представити у вигляді динамічних карт, графіків, таблиць або щось подібне.
4. Розробка і впровадження результатів розробки для різноманітних сценаріїв практичного використання.

## Результати та вплив

Результат проекту може бути використаний громадянами - жителями міст і містечок, органами місцевого самоврядування, насамперед, великих міст або районів важкої промисловості, у якості системи інформування та раннього попередження, для привернення більшої уваги та вжиття своєчасних контрзаходів тощо. 

Запропонована система є розширенням традиційних інструментальних методів моніторингу якості повітря, що сприятиме покращанню своєчасності, повноти і адекватності сприйняття спільнотою інформації про стан навколишнього середовища.

Впровадження результатів проєкту сприятиме ширшому і активнішому залученню членів громади до спостереження, усвідомлення і вирішення питань довкілля.

Внаслідок використання суто інформаційного підходу, результат впровадження проєкту не вимагатиме додаткових матеріальних ресурсів на розбудову інфраструктури, і, таким чином, здійснюватиме мінімально можливий вплив на довкілля.

Успішна реалізація проєкту створює можливості для подальшої реплікації його результатів на різні мови (країни, регіони), інші екологічні фактори, різні соціальні медіа та веб-ресурси.

# **Project concept**

## Problem

Persistent climate change and urban population growth are major factors in deteriorating air quality. The traditional methods of air quality monitoring are the deployment of instrumental monitoring networks.

Although instrumental methods of air quality monitoring demonstrate their high efficiency, in the conditions of modern challenges there are certain problems, which are difficult to overcome within the framework of traditional approaches:

1. it is impossible from practical point of view to achieve the required (desired, sufficient) spatial density of sensors;
2. the vast majority of sensors are able to measure a rather limited list of physical factors that determine air quality, so the AQI obtained by them is often incomplete and, therefore, inadequate;
3. overcoming the problems in pp. 1 and 2 requires the deployment of additional infrastructure and its maintenance and therefore significant resources.

## Idea

The scale of human activity in the global network is impressive, in particular:

- 4.80 billion people around the world use the internet in July 2021 – that’s almost 61% of the world’s total population (according to [Datareportal](https://datareportal.com/global-digital-overview)).
- Facebook daily active users (DAUs) were 1.88 billion as of March 2021 (according to [Facebook Reports First Quarter 2021 Results](https://investor.fb.com/investor-news/press-release-details/2021/Facebook-Reports-First-Quarter-2021-Results/default.aspx)).
- On average, 500 million tweets are shared every day (according to [Twitter by the Numbers (2021): Stats, Demographics & Fun Facts](https://www.omnicoreagency.com/twitter-statistics/)).

Given that, if even a small percentage of these data is devoted to the current state of the environment, analyzing this data, one can provide a huge auxiliary source of information that can significantly expand the capabilities of instrumental methods.

?> The main idea of the project ***AirScape*** is to extend instrumental air quality monitoring networks by alternative means based on social media data (SMD) analysis with the use of geolocalization, text classification, sentiment analysis and other methods of natural language processing (NLP), machine learning (ML), etc.

## Advantages

The main advantages of the proposed approach are:

1. much wider and denser spatial coverage with the ability to quicker respond to critical changes;
2. a more comprehensive list of possible assessed physical factors that affect the air quality, as well as the state of the environment as a whole;
3. no need to deploy additional instrumental (hardware) infrastructure on the ground.

Thus, the project can be considered as a feasibility study for the expansion of instrumental (hardware) air quality monitoring systems by non-traditional methods.

## Plan

The general tentative plan of development envisages building of the following technological chain:

1. Collection of SMD (posts, tweets) according to certain criteria, first of all, georeference (certain region, city, district of the city), time period, availability of keywords, etc.
2. Analysis of the collected SMD (possibly using NLP) to obtain the forming factors and emotions that arise as a result of human response to the environment.
3. The results of SMD analysis will be compared with the results of corresponding instrumental measurements and assessments of air quality by ML means, for further independent use of the results of SMD analysis, especially when and where the results of instrumental methods are absent. So, eventually the results can be presented in the form of dynamic maps, graphs, tables or something similar.
4. Designing and implementing the developed results for various scenarios of practical use.

## Outcomes and impact

The result of the project can be used by citizens - residents of cities and towns, local governments, especially large cities or areas of heavy industry, as a system of information and early warning, to attract more attention and take timely countermeasures and more. 

The proposed system is an extension of traditional instrumental methods of air quality monitoring, which will improve the timeliness, completeness and adequacy of community perception of information about the state of the environment.

The implementation of the project results will promote wider and more active involvement of community members in monitoring, understanding and addressing environmental issues.

Due to the use of a purely informational approach, the result of the project implementation will not require additional material resources for infrastructure development, and thus will have the minimum possible impact on the environment.

Successful implementation of the project creates opportunities for further replication of its results for different languages (countries, regions), other environmental factors, various social media and web resources.

<!-- tabs:end -->
