# Тестування *polyglot*

## Характеристики

*Polyglot* - це безкоштовне програмне забезпечення: ліцензія GPLv3, споряджене
документацією: http://polyglot.readthedocs.org.

*Polyglot* - це конвеєр обробки природної мови (ОПМ, *англ* natural language processing NLP), що підтримує багато мов:

- Токенізація (165 мов)
- Виявлення мови (196 мов)
- Розпізнавання іменованої особи (40 мов)
- Частина позначення мовлення (16 мов)
- Аналіз настроїв (136 мов)
- Вбудовування слів (137 мов)
- Морфологічний аналіз (135 мов)
- Транслітерація (69 мов)

У кожному з представлених функціоналів наявна українська мова.

Матеріал цієї статті базується на оригінальній статті [Python Packages for NLP-Part 1 | by Himanshu Sharma | Towards Data Science](https://towardsdatascience.com/python-packages-for-nlp-part-1-2d49126749ef)

Код прикладу розміщений у форматі Юпітер Ноутбук (*jupyter notebook*) тут [../src/polyglot.md](https://github.com/protw/airscape/blob/master/docs/polyglot.md)

## Встановлення *polyglot* та інших бібліотек

!> **На жаль, на локальному комп'ютері під Windows не вийшло все так прямолінійно, як хотілось - багато бінарних файлів в бібліотеках або не скомпільовані або скомпільовані під інші версії, що створює помилки і завдає багато зайвого клопоту, щоб налаштовувати все вручну!** 
>
> **Здається, що під ОС Linux все має встановлюватись без проблем. Але це треба перевірити.**

Для цієї статті ми використали *Google Colab*. Код нижче встановлюємо *polyglot* та інші необхідні бібліотеки. Встанавлення пройшло гладко.

```python
!pip3 install polyglot
!pip3 install pyicu
!pip3 install pycld2
!pip3 install morfessor
```

Після встановлення бібліотек вище також потрібно встановити деякі функції поліглоту, що використовуватимуться у цій статті.

```python
!polyglot download embeddings2.en
!polyglot download pos2.en
!polyglot download ner2.en
!polyglot download morph2.en
!polyglot download sentiment2.en
!polyglot download transliteration2.hi
```

Також встановимо модуль української транслітерації

```python
!polyglot download transliteration2.uk
```
Імпортуємо необхідні модулі:

```python
import polyglot
from polyglot.detect import Detector
from polyglot.text import Text, Word
from polyglot.mapping import Embedding
from polyglot.transliteration import Transliterator
```

## Виконання операцій ОПМ

Давайте почнемо з вивчення деяких функціональних можливостей ОПМ, що надає *polyglot*. Але перед тим введемо деякі зразки даних, над якими будемо працювати.

```python
sample_text = '''Piyush is an Aspiring Data Scientist and is working hard to get there. He stood Kaggle grandmaster 4 year consistently. His goal is to work for Google.'''
sample_text_ukr = '''Мовлення як вид людської діяльності завжди зорієнтоване на виконання певного комунікативного завдання. Висловлюючи думки і почуття, людина ставить конкретну мету — щось повідомити, про щось переконати тощо. Існує багато визначень тексту.'''
```

### Виявлення мови

Детектор мови в *polyglot* може легко ідентифікувати мову, на якій написаний текст.

```python
# Language detection
detector = Detector(sample_text)
print(detector.language)
detector = Detector(sample_text_ukr)
print(detector.language)
```

### Речення та слова

Для того, щоб витягнути речення або слова з тексту/корпусу, ми можемо використовувати функції *polyglot*.

```python
# Tokenize
text = Text(sample_text)
text.words
text.sentences
```

### Відмічання частин мови

Відмічання (*англ.* tagging) частин мови (*англ.* part of speech, PoS) є важливою операцією ОПМ, що допомагає нам зрозуміти текст та його позначення тегами.

```python
# POS tagging
text.pos_tags
```

### Розпізнавання іменованої особи/об'єкта

Розпізнавання іменованої особи (*англ.* Named Entity Recognition, або NER) використовується для ідентифікації особи, організації та місцезнаходження, якщо такі є у наборі даних корпусу/тексту.

```python
# Named entity extraction
text.entities
```

### Морфологічний аналіз

```python
# Morphological Analysis
words = ["programming", "parallel", "inevitable", "handsome"]
for w in words:
     w = Word(w, language="en")
     print(w, w.morphemes)
```

### Аналіз настроїв

Ми можемо проаналізувати настрій речення.

```python
# Sentiment analysis
text = Text("Himanshu is a good programmer.")
for w in text.words:
   print(w, w.polarity)
```

### Транслітерація

Ми можемо транслітерувати текст між різними мовами.

```python
# Transliteration
transliterator = Transliterator(source_lang="uk", target_lang="en")
new_text = ""
for i in "Всім привіт і до побачення !".split():
  new_text = new_text + " " + transliterator.transliterate(i)
new_text
```
