## centroid_util.py

import re
import numpy as np
import folium
from folium.features import DivIcon
import sys
from pygeodesy.sphericalNvector import meanOf, LatLon

## Розібрати вхідний текст - витягнути пари гео координат з тексту і
## створити список пар координат типу float.
## Аргументи:
##    'text' - вхідний текст;
##    'format_id' 
##        0 - десяткова крапка, кома - "46.737364, 32.812807" (default); 
##        1 - десяткова кома, слеш - "46,737364 / 32,812807";
##        2 - десяткова кома, пробіл - "46,737364 32,812807";
##    'lat_lon_order' - 'LatLon' (default) або 'LonLat'.
## Повертає список пар координат типу float, порядок коорд [Lat,Lon].

def parse_text(text, format_id=0, lat_lon_order='LatLon'):
    format_masks = [
        r'(\d{1,3}\.\d+)\s*\,\s*(\d{1,3}\.\d+)', # 46.737364, 32.812807
        r'(\d{1,3}\,\d+)\s*/\s*(\d{1,3}\,\d+)',  # 46,737364 / 32,812807
        r'(\d{1,3}\.\d+)\s+(\d{1,3}\.\d+)'       # 46.7373 32.8128
    ]
    mask = format_masks[format_id]
    # Повертає список пар (кортежей) координат типу str
    st = re.findall(mask, text)
    # Міняє кому на крапку в кожному елементі
    if format_id == 1:
        sl = [[c.replace(',','.') for c in p] for p in st]
    else:
        sl = [[c for c in p] for p in st]
    # Конвертує елементи str у float, встановлює порядок коорд [Lat,Lon]
    if lat_lon_order == 'LatLon':
        fl = [[float(s[0]), float(s[1])] for s in sl]
    elif lat_lon_order == 'LonLat':
        fl = [[float(s[1]), float(s[0])] for s in sl]
        
    return fl

## Порахувати для відстані: 
##    середнє, 
##    заданий персентіль (75% за замовчанням)

def dist_stats(dist_l, perctl=75):
    dist = {}
    dist_a = np.array(dist_l)
    dist['mean'] = np.mean(dist_a)
    dist['perc'] = np.percentile(dist_a, perctl,
                                 method='interpolated_inverted_cdf')
    return dist

## Побудувати точки з номерами, центроїд, з'єднати центроїд з точками, 
## побудувати коло за розміром персентиля

def show_pnts_on_map(points,map,color='red',labels=[]):
    fstr = '<div style="font-size: 16pt; color: ' + color + '">{}</div>'
    if type(points[0]) is not list: # When there is a single point
        points = [points]
    if labels: # check number of custom labels 
        if len(points) != len(labels):
            print('Кількість міток не збігається з кількістю точок!')
            sys.exit(1)
    else: # set default labels
        labels = [str(i+1) for i,_ in enumerate(points)]
    for i,_ in enumerate(points):
        folium.CircleMarker(location=points[i], color=color, radius=5, 
                            fill=color).add_to(map)
        folium.map.Marker(location=points[i], 
                          icon=DivIcon(icon_size=(150, 36),icon_anchor=(0, 0),
                                       html=fstr.format(labels[i])
        )).add_to(map)
    return map

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

def centroid_main(text, coord_format_id=0, perctl=65, zoom_start=12, 
                  html_page='map_my_2.html'):
    pnts = parse_text(text[coord_format_id],coord_format_id)
    print(f'Кількість точок: {len(pnts):d}')

    if len(pnts) < 2:
        print('Кількість точок менша 2!')
        sys.exit(1)

    ## Знайти центроїд групи точок 'pnts'
    pnts_LL = [LatLon(p[0],p[1]) for p in pnts]
    cntr = meanOf(pnts_LL)

    ## Знайти відстань від центру групи до кожної точки групи
    dist_l = [cntr.distanceTo(p) for p in pnts_LL]

    print(f'Центроїд:\n{cntr.lat:.6f}, {cntr.lon:.6f}')
    print('№, коорд, відстань (м):')
    for i,_ in enumerate(pnts):
        print(f'{i+1:00d}, {pnts[i][0]:.6f}, {pnts[i][1]:.6f}, {dist_l[i]:.1f}')

    dist = dist_stats(dist_l, perctl)
    print(f'Середня відстань (м) - {dist["mean"]:.1f}\n'
          f'{perctl:d}% точок розміщені у колі діаметром {2*dist["perc"]:.1f} м')

    ## Побудувати точки з номерами, центроїд, з'єднати центроїд з точками, 
    ## побудувати коло за розміром персентиля

    cntr_l = [cntr.lat, cntr.lon]

    m = folium.Map(location=cntr_l, zoom_start=zoom_start, 
                   tiles='openstreetmap')

    m = show_pnts_on_map(pnts,m,color='red')
    m = show_pnts_on_map(cntr_l,m,color='blue',labels=['Центр'])

    # З'єднати центроїд з точками
    for i,_ in enumerate(pnts):
        folium.PolyLine(locations=[pnts[i],cntr_l], color='red').add_to(m)

    folium.Circle(cntr_l, radius=dist['perc']).add_to(m)

    ## Зберегти і відобразити веб сторінку

    m.save(html_page)
