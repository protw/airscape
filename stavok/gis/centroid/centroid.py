'''
Завдання:
    Знайти центроїд групи гео точок, розмір групи, відобразити на мапі
Порядок дій:
    1) простий інтерфейс для введення вхідних даних і параметрів
    2) розбрати текст - знайти в ньому пари чисел (шир, довг) 
    3) знайти центроід знайдених точок та статистично визначений розмір групи
    4) підготувати дані для зчитування
    5) відобразити на карті точки і розмір області
'''
## Підключити бібліотеки

import webbrowser
from centroid_util import centroid_main

if __name__ == "__main__":
    ## Параметри
    coord_format_id = 0
    perctl = 65
    zoom_start = 12
    html_page = 'map_my_2.html'

    text = ['''
        Lorem ipsum dolor sit amet, consectetur 46.736906, 32.810302 adipiscing 
        elit, sed do 46.737364,  32.812807 eiusmod tempor incididunt 123.987 ut 
        labore et dolore 46.739309, 32.807631 magna aliqua. Quam 345.678,34 quisque 
        id diam vel quam elementum. Mauris augue neque 46.740682, 32.802510 gravida 
        in fermentum et sollicitudin ac. 46.734260,32.811582 Imperdiet dui accumsan 
        sit amet. Risus sed vulputate odio ut enim.''',
        '''
        Lorem ipsum dolor sit amet, consectetur 46,736906/ 32,810302 adipiscing 
        elit, sed do 46,737364/  32,812807 eiusmod tempor incididunt 123,987 ut 
        labore et dolore 46,739309/ 32,807631 magna aliqua. Quam 345,678/34 quisque 
        id diam vel quam elementum. Mauris augue neque 46,740682/ 32,802510 gravida 
        in fermentum et sollicitudin ac. 46,734260/32,811582 Imperdiet dui accumsan 
        sit amet. Risus sed vulputate odio ut enim.''',
        '''
        АБВГД 48.01388889 38.79638889 07:59 АБВГД 48.01416667 38.90555556 07:53
        АБВГД 50.02583333 36.62444444 07:53 АБВГД 48.02972222 38.96805556 07:53
        АБВГД 48.00027778 38.25944444 07:52 АБВГД 48.02416667 38.23111111 07:52
        АБВГД 47.02138889 38.19 07:49 АБВГД 45.00166667 35.62611111 07:47
        АБВГД 46.03694444 35.53361111 07:46 АБВГД 45.01694444 32.87138889 07:41
        АБВГД 45.01527778 36.95694444 07:37 АБВГД 45.0175 32.87888889 07:35
        АБВГД 45.03055556 36.27305556 07:32 АБВГД 46.00333333 33.52361111 07:30
        АБВГД 45.01777778 32.87194444 07:27 АБВГД 45.03388889 33.80055556 07:10
        АБВГД 48.01777778 39.56805556 07:05 АБВГД 47.01833333 38.14944444 07:02
        АБВГД 48.02972222 39.27527778 07:02 АБВГД 47.03722222 38.12 07:01
        ''']

    centroid_main(text, coord_format_id=coord_format_id, perctl=perctl, 
                  zoom_start=zoom_start, html_page=html_page)

    webbrowser.open(html_page)

