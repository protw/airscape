# parse_cmd_line.py

"""
'parse_cmd_line.py' reads command line arguments for 'form2csv.py'. 
The code is based on famous library `argparse`.

usage: parse_cmd_line.py [-h] [-f [FORM_DIR ...]] [-c [OUTPUT_CSV]] 
                         [-d [OUTPUT_DIR ...]]

Collecting data from multiple PDF forms into single CSV table

optional arguments:
  -h, --help            show this help message and exit
  -f [FORM_DIR ...], --form_dir [FORM_DIR ...]
                        PDF forms' folder (default: empty, than GUI is called)
  -c [OUTPUT_CSV], --output_csv [OUTPUT_CSV]
                        Output CSV file name (default: the same as 'forms_folder')
  -d [OUTPUT_DIR ...], --output_dir [OUTPUT_DIR ...]
                        Directory for output CSV file (default: empty, than 1 
                        level up 'forms_dir'..)

Usage inside code:
    
    import sys
    from parse_cmd_line import fetch_cli_args

    args = fetch_cli_args()
    if args['cancelled']:
        print('Inputting cancelled!')
        sys.exit()
    form_dir   = args["form_dir"]
    output_csv = '/'.join([args["output_dir"], args["output_csv"]])
"""

import argparse
import os
import re
from select_folder import select_folder

def set_parser():
    parser = argparse.ArgumentParser(description='Collecting data from multiple'
                                     ' PDF forms into single CSV table')
    parser.add_argument(
        '-f',
        '--form_dir',
        default='.\\',
        nargs='*',
        required=False,
        help='PDF forms\' folder (default: empty, than GUI is called)'
    )
    parser.add_argument(
        '-c',
        '--output_csv',
        default='',
        nargs='?',
        help='Output CSV file name (default: the same as \'forms_folder\')'
    )
    parser.add_argument(
        '-d',
        '--output_dir',
        default='',
        nargs='*',
        help='Directory for output CSV file (default: empty, than 1 level up'
             ' \'forms_dir\'..)'
    )

    return parser.parse_args()

def fetch_cli_args(initialdir='./'):

    parsed_cli = set_parser()

    # --form_dir
    # '-f' omitted or '-f' with empty str list -> GUI
    if (type(parsed_cli.form_dir) is str) or \
       len(parsed_cli.form_dir) == 0:
        title = 'Select PDF form folder'
        form_dir = select_folder(title=title, initialdir=initialdir)
        if len(form_dir) == 0: # GUI cancelled -> stop execution
            return {'cancelled': True}
    else:
        form_dir = os.path.abspath(parsed_cli.form_dir[0])

    # --output_csv
    if not parsed_cli.output_csv: # '-c' omitted -> 
        output_csv = os.path.basename(form_dir)
        # if 'form_dir' ends with '\' or '/' than 'output_csv' is empty string
        if not output_csv:
            # cut tailing '\' or '/'
            form_dir = re.sub('[/\\\]+$','',form_dir)
        output_csv = os.path.basename(form_dir) + '.csv'
    else:
        output_csv = parsed_cli.output_csv
        if output_csv.split('.')[-1].lower() != 'csv': 
            output_csv += '.csv'

    # --output_dir
    form_dir_ = '/'.join(re.split('[\\\\/]',form_dir)[:-1])
    if len(form_dir_) == 0: # 'form_dir' is root (most upper) folder
        return {'cancelled': True}
    if type(parsed_cli.output_dir) is str: # '-o' omitted -> 1 level up 'forms_dir\..'
        output_dir = form_dir_
    elif len(parsed_cli.output_dir) == 0: # '-o' with empty str list -> GUI
        title = 'Select folder for output CSV'
        output_dir = select_folder(title=title, initialdir=form_dir_)
        if len(output_dir) == 0: # GUI cancelled -> stop execution
            return {'cancelled': True}
    else:
        output_dir = os.path.abspath(parsed_cli.output_dir[0])

    return {'form_dir': form_dir, 'output_csv': output_csv, 
            'output_dir': output_dir, 'cancelled': False}

if __name__ == '__main__':

    import sys
    
    args = fetch_cli_args()

    if args['cancelled']:
        print('Inputting cancelled!')
        sys.exit()
        
    print(f'form_dir   = {args["form_dir"]}')
    print(f'output_csv = {args["output_csv"]}')
    print(f'output_dir = {args["output_dir"]}')

