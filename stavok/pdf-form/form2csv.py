#!/usr/bin/env python
# coding: utf-8

# # Автоматизована обробка PDF форм
# 
# Якщо ви не є щасливим власником Adobe Acrobat або ABBY Finereader, то для автоматизованої обробки великої кількості анкет у форматі PDF форм вам в нагоді стане цей код.
# 
# Анкети та опитувальники у форматі PDF форм вважаються більш традиційними у порівнянні з купою інструментів для створення онлайн форм. Для PDF форм вам не треба дбати про підтримку веб-середовища і ви можете заповнювати форму офлайн. Ви можете розсилати форми електронною поштою. Зазвичай PDF форма розміщає поля компактніше і згодом ви можете роздрукувати заповнену форму. Все це виглядає традиційніше і надійніше - саме це може приваблювати багатьох користувачів.
# 
# Попутньо може виникнути питання - чим же створювати PDF форми? На щастя відповідь є. Пошук в інтернеті надасть вам купу онлайн і офлайн інструментів для створення PDF форми.

# ## Отже перейдемо до справ
# 
# Постановка завдання виглядає так: у нас в окремому фолдері зібрані однакові заповнені форми; нам потрібно зібрати всі введені дані у одну таблицю, де кожна колонка відповідає окремому полю і кожний рядок - окремому файлу PDF форми.
# 
# Одразу розпочнімо до клювого компонента - це модуль `fetch_form_fields.py `, призначений для отримання значень всіх полів з однієї PDF форми. Код цього модулю [розміщений тут](https://github.com/protw/airscape/blob/master/stavok/pdf-form/fetch_form_fields.py) і безпосередньо запозичений з деякими доопрацюваннями з [документації пакету `pdfminer`](https://pdfminersix.readthedocs.io/en/latest/howto/acro_forms.html), де алгоритм дуже ретельно пояснений, так що потреби повторювати ці пояснення вже немає.
# 
# ## Використані модулі

# In[1]:


import glob
import os
import csv
import pandas as pd
import sys
from fetch_form_fields import fetch_form_fields
from parse_cmd_line import fetch_cli_args


# ## Файл для збирання табличних даних
# 
# Для зручності ім'я файлу зібраних табличних даних збігається з іменем відповідного фолдеру з формами. Скажімо, ми маємо два фолдери `form_folder_1` і `form_folder_2`, що містять 2 різних набори заповнених форм. В такому разі файли зібраних табличних даних матимуть такі імена `form_folder_1.csv` і `form_folder_2.csv`. У підсумку файлова структура даних матиме такий вигляд: 
# 
# ![](form_data_structure.png)
# 
# Тепер можна формувати ім'я файлу зібраних табличних даних:

# In[3]:


# Data folder containing similar PDF forms
initialdir = '.'
             
args = fetch_cli_args()
if args['cancelled']:
    print('Inputting cancelled!')
    sys.exit()
form_dir   = args["form_dir"]
output_csv = '/'.join([args["output_dir"], args["output_csv"]])


# Відкриваємо файл для збирання табличних даних:

# In[4]:


#open new csv file
out_file = open(output_csv, 'w+')
writer = csv.writer(out_file)


# ## Основний цикл збирання табличних
# 
# Цей цикл проводиться за списком файлів PDF форми, що створюється методом `glob.glob(pathname)`, що повертає список шляхів, які відповідають шаблону `pathname`. Шлях може бути як абсолютним так і відносним.
# 
# Першим кроком функція `fetch_form_fields(filename)` повертає словник `data`, що містить всі поля однієї форми `filename`. Зі словника ми робимо два списки: список ключів `head` для заголовку таблиці і список значень `row` для рядка даних цієї таблиці.
# 
# До кожного з двох списків додаємо на початок елемент що містить ім'я файлу PDF форми.
# 
# Список заголовку `header` ми записуємо один раз на першій ітерації (коли заголовок порожній `if not header`) та запам'ятовуємо у множині `header_set` для наступних порівнянь. На всіх наступних ітераціях ми проводимо перевірку поточного списку заголовка `head` на збіг зі списком заголовку з першого PDF файлу. Якщо поточний заголовок не збігається, то цей рядок буде пропущений і не буде записаний. Також буде видано попередження про відсутність збігу у поточному PDF файлі.

# In[5]:

print(f'FORM2CSV reading form data folder "{form_dir}"')
n_skipped = 0
file_list = glob.glob(os.path.join(form_dir, '*.pdf'))

def collect_data():
    header = [] # header row
    for filename in file_list:
        
        data = fetch_form_fields(filename) # returns dictionary
        
        filename_i = os.path.basename(filename)
        head = list(data.keys())
        row = list(data.values())
        if not header: # get header from the first file
            header = head.copy()
            header.insert(0,'file_name') # insert column with file name
            writer.writerow(header)
            header_set = set(head) # for further comparison
            filename_0 = filename_i
        else: # check whether the rest of files have the same fields' list
            if header_set != set(head): # if not the same - skip this record
                print(f'WARNING! Set of fields in "{filename_i}"'
                      f' differs from  "{filename_0}"')
                n_skipped += 1
                continue
        row.insert(0,filename_i) # insert column with file name
        writer.writerow(row)

collect_data()

# ## Заключні кроки
# 
# Після завершення циклу не забуваймо закрити файл для збирання табличних даних і підвести статистичні підсумки:

# In[6]:


out_file.close()

n_total_forms_number = len(file_list)
print(f'-- Form data collected in table "{output_csv}"')
print(f'-- Total number of forms: {n_total_forms_number}')
print(f'-- Number of forms collected: {n_total_forms_number-n_skipped}')
print(f'-- Number of forms skipped: {n_skipped}')


# В зв'язку з тим, що у нашому випадку ми маємо вміст кирилицею і латиною, то для коректного відображення, зокрема, у Excel необхідно конвертувати текстовий CSV файл у `UTF BOM`.

# In[7]:


# Convert 'output_csv' to UTF-8 BOM in order 
# to make cyrillic text readable in Excel
df = pd.read_csv(output_csv, sep=',')
df.to_csv(output_csv, sep=',', encoding="utf-8-sig",index=False)

df.head()

print('DONE!')


# Це все. Користуйтесь на здоров'я.
