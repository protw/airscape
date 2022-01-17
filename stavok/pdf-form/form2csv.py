import glob
import os
import csv
import pandas as pd
import re
from fetch_form_fields import fetch_form_fields

def output_csv_name(form_dir):
    output_csv = os.path.basename(form_dir)
    # if 'form_dir' ends with '\' or '/' than 'output_csv' is empty string
    if not output_csv:
        # cut tailing '\' or '/'
        form_dir = re.sub('[/\\\]+$','',form_dir)
        output_csv = os.path.basename(form_dir)
    return output_csv + '.csv'

# Data folder containing similar PDF forms
form_dir = 'D:\\boa_dev\\pyt\\pdf-form\\form-02\\'

output_csv = output_csv_name(form_dir)

#open new csv file
out_file = open(output_csv, 'w+')
writer = csv.writer(out_file)

header = [] # header row
for filename in glob.glob(os.path.join(form_dir, '*.pdf')):
    
    data = fetch_form_fields(filename)
    
    filename_i = os.path.basename(filename)
    head = list(data.keys())
    row = list(data.values())
    if not header: # get header from the first file
        header = head
        header.insert(0,'file_name')
        writer.writerow(header)
        header_set = set(header) # for further comparison
        filename_0 = filename_i
    else: # check whether the rest of files have the same fields' list
        if header_set != set(head): # if not the same - skip this record
            print(f'WARNING! Set of fields in "{filename_i}"'
                  f' differs from  "{filename_0}"')
            continue
    row.insert(0,filename_i)
    writer.writerow(row)

out_file.close()

# Convert 'output_csv' to UTF-8 BOM in order 
# to make cyrillic text readable in Excel
df = pd.read_csv(output_csv, sep=',')
df.to_csv(output_csv, sep=',', encoding="utf-8-sig",index=False)
