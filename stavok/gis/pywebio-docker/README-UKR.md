# Ще один веб-додаток на Docker

Це шаблон розгортання гео веб-застосунку на основі *Python* на *Docker* з використанням пакетів `pywebio`, `yaml`, `folium` і `pygeodesy`.

![докер-пітон](docker-python.png)

## Опис завдання

> Сутність власне завдання у нашому розгляді не важливо. Воно сформульовано тут для прикладу. У майбутньому на основі цього підходу можуть бути реалізовані інші завдання та рішення.

**Завдання**: Дано текст, що містить опис із переліком геолокацій. Координати точок можуть бути записані у тексті в різних форматах і мати різний порядок широти та довготи (Lat, Long або Long, Lat). Необхідно витягти з тексту координати всіх точок, знайти їхню центральну точку і відобразити всі точки включно із центральною на мапі на веб-сторінці. Застосунок, що генерує цю мапу, має бути портабельний, тобто не залежати від операційної системи комп'ютера, на якому його розгорнуто. Також цей застосунок має оприлюднювати цю мапу у відкритий простір у вигляді веб сторінки. 

## Особливості коду

Деякі істотні особливості рішення:

- інтерфейс користувача та веб-сервіс базуються на пакеті  `pywebio`;
- інтерфейс користувача визначено у `yaml` файлі, дані з якого перетворюються на словник *Python*;
- аргументи для функцій інтерфейсу користувача передаються з допомогою [механізму розпакованого словника](https://python-reference.readthedocs.io/en/latest/docs/operators/dict_unpack.html) ;
- мапа генерується і відтворюється з допомогою пакету `folium`;
- геодезичні обчислення проведені з допомогою пакету `pygeodesy`.

## Файли та їх призначення

Тут наведений повний перелік файлів, необхідних для нашого рішення:

- `centroid_calc_pywebio.py`– основний скрипт;
- `centroid_pars.yml`– специфікація елементів інтерфейсу користувача;
- `centroid_util.py`– основні геодезичні обчислення і формування карти;
- `Dockerfile`– інструкції зі створення образу і запуску контейнера *Docker*;
- `README.md`– опис рішення англійською, також є опис українською у `README-UKR.md`;
- `requirements.txt`– список пакетів *Python* для створення образу *Docker*.

## Короткий опис коду

### Основний скрипт

Основний скрипт розміщений у файлі `centroid_calc_pywebio.py`. Спочатку імпортуємо всі необхідні пакети:

```python
from pywebio.output import put_text, put_markdown, put_html, put_button, use_scope
from pywebio.pin import put_select, put_textarea, pin, pin_wait_change
from pywebio import start_server

from centroid_util import centroid_main

import yaml
```

Потім завантажуємо специфікацію інтерфейсу користувача з файлу `'centroid_pars.yml'`та конвертуємо її у словник `in_pars`:

```python
yml_file = 'centroid_pars.yml'

with open(yml_file, "r") as file:
    in_pars = yaml.load(file, Loader=yaml.FullLoader)
    # Forming the variables for further use
    coord_format_help_md = in_pars['coord_format_help_md']
    coord_format_options = in_pars['coord_format']['options']
    in_pars.pop('coord_format_help_md') # delete unusable key otherwise it's error
```

Тут відмітимо важливий момент: усі ключі в словнику точно відповідають назвам аргументів методів введення. Таким чином, відповідні значення словника будуть належним чином передані як значення аргументів до методів введення. Про це нижче.

Виконання геодезичних обчислень, а також формування карти та результуючого тексту виконується функцією `disp_html`. Ця функція використовується як зворотний виклик (callback) у кнопці ініціювання обчислень і відображення.

```python
def disp_html():
    with use_scope('pars', clear=True):
        coord_format_id = coord_format_options.index(pin.coord_format)

        # Performs calculation, forms 'map' and text result string 't_res'
        map, t_res = centroid_main(pin.text, coord_format_id=coord_format_id,
                               perctl=pin.perctl, zoom_start=pin.zoom_start)
        # Text result output
        put_markdown('# РЕЗУЛЬТАТ')
        put_text(t_res)

        # Displays map
        put_html(map._repr_html_())
```

Важливо відзначити, що всі дії в цій функції  стосовно відображення результатів у бравзері виконуються в певній області видимості, заданій методом `use_scope` з аргументом `clear`, значення якого встановлено на `True` з тим, щоб очищати область видимості щоразу, коли викликається метод.

Вся структура веб-інтерфейсу показана простим, але ефективним способом у методі `app` з допомогою методів `pywebio`:

```python
def app():
    # Display header
    put_markdown(coord_format_help_md)
    put_markdown('# ВХІДНІ ПАРАМЕТРИ')

    # Render input elements, input arguments are passed via 
    # unpacked dict instead of plain list
    put_select(**in_pars['coord_format'])
    put_select(**in_pars['lat_lon_order'])
    put_select(**in_pars['perctl'])
    put_select(**in_pars['zoom_start'])
    put_textarea(**in_pars['text'])
    
    # Launch calculation, display map and text result
    put_button('РАХУВАТИ', onclick=lambda: disp_html())
```

Насправді тут можна побачити три очевидні частини: заголовок, п’ять елементів введення та кнопку, що власне запускає обчислення та відображення результату.

У другому блоці цього фрагмента для передачі фактичних значень аргументів використовується [механізм розпакованого словника . ](https://python-reference.readthedocs.io/en/latest/docs/operators/dict_unpack.html)Коли ви дослідите специфікації елементів інтерфейсу користувача у файлі `'centroid_pars.yml'`, то помітите всередині п’ять вкладених словників із такими назвами: `'coord_format'`, `'lat_lon_order'`, `'perctl'`, `'zoom_start'` і `'text'`. Усі елементи (keys) всередині цих п'яти словників названі в точній відповідності до аргументів, використаних у методах введення: `put_select` і `put_textarea`.

### Специфікація елементів інтерфейсу користувача

Файл `'centroid_pars.yml'` містить специфікацію п'яти елементів інтерфейсу користувача. Тут нижче представлені два з цих п'яти. Формат YAML є найбільш читабельним, тому пояснення не потрібні (особливо після ознайомлення з документацією `pywebio`):

```yaml
coord_format:
  label: Формат координат
  options:
    - "46.7373, 32.8128"
    - "46,7373 / 32,8128"
    - "46.7373 32.8128"
  value: "46.7373, 32.8128"
  name: coord_format
lat_lon_order:
  label: Порядок координат
  options:
    - LatLon
    - LonLat
  value: LatLon
  name: lat_lon_order
```

### Основні геодезичні обчислення і формування мапи

Основні геодезичні обчислення і формування мапи здійснюється кодом у `centroid_util.py`. Оскільки ця стаття описує питання розгортання веб-застосунку, немає сенсу заглиблюватися в пояснення цього коду.

Лише зазначимо, що всередині є всього чотири методи:

- `parse_text`– аналізує вхідний текст – витягує геокоординатні пари з тексту та створює їхній список;
- `dist_stats`– обчислює деяку статистику для відстаней від точок до центральної точки;
- `show_pnts_on_map`– будує точки на мапі із супровідною інформацією;
- `centroid_main`– цей метод розташовує всі методи в цьому файлі в логічному порядку.

### Докеризація коду

Перш ніж почати докеризувати свої розробки, так чи інакше вам доведеться прочитати хоча б пару популярних статей на цю тему. Після прочитання код Dockerfile, наведений нижче, стане вам цілком зрозумілим і, тому, немає сенсу в зайвих буквах:

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

CMD python centroid_calc_pywebio.py
```

## Створення та розгортання програми

Після всього описаного вище створити та розгорнути наш застосунок в Docker так само просто, як показано нижче.

Створіть образ Docker:

```shell
docker build --tag python-docker .
```

Запустіть зображення як контейнер:

```shell
docker run -p 8080:8080 python-docker
```

Запуск контейнера в браузері на http://localhost:8080

## Заключне слово

Представлений код був повністю протестований і працездатний.

Тому насолоджуйтесь на здоров'я: читайте, модифікуйте, експериментуйте.

 
