# Глосарій NLP

Демістифікація галузі обробки природної мови (*natural language processing* — NLP) починається з роз’яснення базових термінів.

Цей глосарій є перекладом статті автора *Mandy Gu* [NLP Glossary for Beginners](https://medium.com/analytics-vidhya/nlp-glossary-for-beginners-c3093529ee4). 

Обробка природних мов (ОПМ або NLP) звучить набагато страшніше, ніж такою є. Насправді, основними вимогами до занять у цій галузі є елементарні навички програмування, знання принципів науки про дані та концептуальне розуміння того, як машини обробляють мови.

Цей глосарій зосереджений на обробці природних **писемних** мов.

# 1. Загальні поняття

## Обробка природної мови

:gb: *Natural Language Processing (NLP)*

NLP - це сфера машинного навчання, орієнтована на людські мови. Сюди входять як писемна, так і розмовна мови.

## Словник

:gb: *Vocabulary*

Весь набір термінів, що використовуються у тілі тексту.

## Поза словником

:gb: *Out of Vocabulary*

У NLP дані, що використовуються для навчання нашої моделі, складаються з обмеженої кількості словникових термінів. Дуже часто ми стикаємось зі позасловниковими термінами, коли використовуємо нашу модель для обробки нових текстів. Як правило, для цих термінів призначається загальний замінник.

## Корпус

:gb: *Corpus (множина - Corpora)*

Корпус - це сукупність текстів. Корпус може являти собою збір оглядів фільмів, коментарів в Інтернеті або розмов між двома людьми.

## Документи

Документом називають тіло тексту. Сукупність документів утворює корпус. Наприклад, огляд фільму або електронний лист є прикладами документа.

## Попередня обробка

:gb: *Preprocessing*

Першим кроком до будь -якого завдання НЛП є попередня обробка тексту. Мета попередньої обробки - "очистити" текст, видаливши якомога більше шуму. Загальні етапи попередньої обробки описані в розділі *Методи*.

## Токенізація

:gb: *Tokenization*

Процес поділу великого фрагменту тексту на менші частини. Зазвичай це робиться для того, щоб кожну невелику частину або *токен* можна було зіставити зі значущою одиницею інформації. Якщо поділити наданий текст на слова, то кожне слово стає його власною лексемою.

## Вбудовування (слів)

:gb: *Embeddings*

Кожен токен вбудовується як вектор, перш ніж його можна передати в модель машинного навчання. Хоча зазвичай під вбудовуванням розуміють вбудовування слів, також вбудовування можна створювати на рівні символів або фраз. Нижче є окремий розділ щодо різних видів вбудовувань.

## n-грами

:gb: *n-grams*

Суміжна послідовність з *n* лексем у наданому тексті. У фразі *the day is young* маємо такі біграми (*the, day*), (*day, is*), (*is, young*).

## Трансформери

:gb: *Transformers*

У 2017 році була представлена нова архітектура глибокого навчання (*deep learning*), що перевершила декілька попередніх показників результативності для завдань NLP. Трансформери компенсують два недоліки рекурентної нейронної мережі (RNN): здатність паралелізувати обчислення і краще підходять для вивчення довгострокових залежностей між словами.

# 2. Методи

## Частини мови

:gb: *Parts of Speech (POS)*

Синтаксична функція слова. Напевно, всі знайомі з різними частинами мови: іменником, дієсловом, прикметником, прислівником тощо.

## Відмічання частини мови

:gb: *Parts of Speech Tagging*

Процес призначення кожній лексемі в тексті належної мітки частини мови.

## Нормалізація

:gb: *Normalization*

Процес зведення подібних лексем до канонічної форми. Наприклад, якщо ми вважаємо, що *hello* та *Hello* мають однакове значення, ми можемо *нормалізувати* наш текст, звівши обидва терміни у *hello.*

## Стоп-слова

:gb: *Stop Words*

Ці слова відфільтровуються перед будь-яким завданням попередньої обробки або моделювання. Стоп-слова обираються з огляду на їх незначущисть для поточного завдання NLP. Наприклад, список англійських стоп-слів у пакеті `nltk` визначає для виключення такі загальні слова, як-то *a, to, can*.

## Лематизація

:gb: *Lemmatization*

Це метод нормалізації, тобто групування змінених термінів до їхньої базової форми, обумовленої відповідною частиною мови в наданому тексті. Наприклад, і *walking*, і *walked* будуть відображені як *walk*.

## Стемінг

:gb: *Stemming*

Подібно до лематизації, стемінг також зменшує змінені терміни до їхньої базової форми. Єдина відмінність полягає в тому, що мітка частини мови не використовується для визначення базової форми.

> Нотатка щодо лематизації проти стемінгу: ви можете зауважити, навіщо взагалі потрібно використовувати стемінг? Чи не був би цей крок скорочення слова точнішим, якби ми знали його частину мови? Очевидною перевагою стемінгу є те, що він відбувається набагато швидше. Інша полягає в тому, що це виключає похибку, що виникає завдяки автоматичної помічення лексем частинами мови.

# 3. Загальні завдання NLP

## Аналіз настроїв

:gb: *Sentiment Analysis*

Автоматизований процес виявлення емоції з тексту. Поширеним застосуванням аналізу настроїв є визначення чи наданий є відгук позитивним чи негативним, або чи наданий текст підтримує певні почуття.

## Машинний переклад

:gb: *Machine Translation*

Із цим все зрозуміло - усі поширені засоби автоматизованого перекладу є програмами NLP.

## Машинне (читання) розуміння та відповідь на запитання

:gb: *Machine (Reading) Comprehension / Question Answering*

Машинне розуміння, яке зазвичай здійснюється з допомогою відповіді на запитання, - це завдання автоматичного "розуміння" тексту. Зазвичай це перевіряється з допомогою запитань на розуміння прочитаного, де вхідним є контекстуальний документ і набір питань, на які можна відповісти з допомогою документа. Штучний інтелект дає відповіді на основі цих вхідних даних.

## Розпізнавання іменованої сутності

:gb: *Named Entity Recognition (NER)*

Автоматичне виокремлення відповідних сутностей (таких як імена, адреси та телефонні номери) з неструктурованого документа.

## Пошук інформації / Прихована семантична індексація

:gb: *Information Retrieval / Latent Semantic Indexing*

Автоматичне видобування інформації з великої системи (наприклад, у веб-пошукових системах). Проблема визначається як повернення правильного документа (документів) за умови надання конкретного запиту.

# 4. Вбудовування

## Мішок слів

:gb: *Bag of Words (BoW)*

Це найпростіший метод вбудовування слів у числові вектори. Він не часто використовується на практиці через надмірне спрощення мови, але зазвичай зустрічається у прикладах та навчальних посібниках.

Розглянемо такі документи:

- **Документ 1:** *high five*
- **Документ 2:** *I am old.*
- **Документ 3:** *She is five.*

Це дає нам словниковий запас: (*high, five, i, am, old, she, is*). Ігноруємо знаки пунктуації та нормалізуємо лексеми переведенням їх до нижнього регістру. Далі, можна побудувати матрицю, що представляє кількість разів, що кожен словниковий термін зустрічається у документі.

|        | Документ 1 | Документ 2 | Документ 3 |
| :----: | :--------: | :--------: | :--------: |
| *high* |     1      |     0      |     0      |
| *five* |     1      |     0      |     1      |
|  *i*   |     0      |     1      |     0      |
|  *am*  |     0      |     1      |     0      |
| *old*  |     0      |     1      |     0      |
| *she*  |     0      |     0      |     1      |
|  *is*  |     0      |     0      |     1      |

Таким чином, власне отримали *мішок слів*, що представляє як кожне слово, так і документ. Щоб отримати представлення слова, переміщаємось горизонтально, наприклад: *high* - [1, 0, 0]. Щоб отримати представлення документа, переміщаємось вертикально, наприклад: *документ 1* - [1, 1, 0, 0, 0, 0, 0].

## TF-IDF - частота терміну - зворотна частота документа

:gb: *TF-IDF term frequency - inverse document frequency*

На відміну від мішка слів, TF-IDF враховує відносну важливість кожного терміну для документа. Векторне представлення кожного терміна та документа можна отримати схожим до мішка слів чином.

|           |   Документ 1   |   Документ 2   | ...  |
| :-------: | :------------: | :------------: | :--: |
| *термін1* | t<sub>11</sub> | t<sub>12</sub> |      |
| *термін2* | t<sub>21</sub> | t<sub>22</sub> |      |
|    ...    |                |                |      |

Статистика TF-IDF для *i*-го терміну в *j*-му документі зазвичай обчислюється таким чином:

$$
t_{i,j} = TF{-}IDF = TF \cdot IDF
$$
де:
$$
TF(i,j)=\frac{number~of~times~term~i~is~in~document~j}{total~number~of~terms~in~document~j} \\
IDF(i)=\frac{total~number~of~documents}{number~of~documents~containing~term~i}
$$
Вектори документів можуть бути використані як функції для різних моделей машинного навчання, як-то: SVM, Naive Bayes, Logistic Regression ... тощо.

## word2vec

Навчаючись на великих корпусах, *word2vec* використовує неглибоку нейронну мережу для визначення семантичного та синтаксичного значення за спільним входженням слова. 

*word2vec* створює високовимірний простір ознак. Такі складніші вбудовування добре підходять для рекурентних нейронних мереж (RNN), де також враховується порядок слів.

## Контекстозалежні вбудовування

:gb: *Context Dependent Embeddings*

Вбудовування word2vec не залежать від контексту - кожне слово буде відображено в одному і тому ж векторі, незалежно від навколишнього контексту. Такі вставки, як *BERT*, *ELMo*, створюють вбудовування слів, що змінюються залежно від контексту фрази.

# 5. Популярні бібліотеки Python

## sklearn

*sci-kit learn* надає набір корисних опцій для вбудовування, включаючи *BoW* та *TF-IDF*. Усі ці функції поставляються з можливістю налаштування векторизаторів, включаючи побудову термінів з використанням n-грамів та виключення незвичайних термінів.

## keras / tensorflow / pytorch

Моделювання мови має послідовний компонент. Порядок слів має велике значення. Таким чином, моделі глибокого навчання, такі як рекурентні нейромережі (RNN), неймовірно популярні для завдань NLP.

## nltk

*nltk*, що розшифровується як *Natural Language Toolkit* , пропонує кілька інструментів навколо NLP, що полегшує попередню обробку. Він поставляється з кількома стемерами, лематизаторами, токенізаторами та детокенізаторами. Однією з переваг *nltk* є те, що він підтримує кілька різних алгоритмів для кожної функції - він чудово підходить для дослідження та для розуміння того, що відбувається у бекенді.

## spaCy

Як і *nltk*, *spaCy* це бібліотека загального призначення для попередньої обробки тексту. *spaCy* пропонує підтримку більшої кількості мов і перевершує *nltk* у більшості порівняльних показників.