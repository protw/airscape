# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 11:02:12 2021

@author: https://protw.github.io/oleghbond
"""

import csv
import pandas as pd

def sortFreqDict(freq_dict):
    freq_list = [(freq_dict[key], key) for key in freq_dict]
    freq_list.sort()
    freq_list.reverse()
    dict_sorted = {}
    for item in freq_list:
        dict_sorted[item[1]] = item[0]
    return dict_sorted

def dict2csv(a_dict, csv_file):
    a_file = open(csv_file, 'w')
    writer = csv.writer(a_file,lineterminator='\r')
    for key, value in a_dict.items():
        writer.writerow([key, value])
    a_file.close()

    # Change encoding of CSV file in order clyrillic text readability
    df = pd.read_csv(csv_file, sep=',', encoding='utf-8', \
                     names=['Term', 'Freq'])
    df.to_csv(csv_file, sep=',', encoding="utf-8-sig", index=False)

"""
a_dict = sortFreqDict(word_freq)
csv_file = 'word_freq_zel.csv'
dict2csv(a_dict, csv_file)
"""
