# -*- coding: utf-8 -*-

## IMPORT OF MODULES

from pywebio.output import put_text, put_markdown, put_html, put_button, use_scope
from pywebio.pin import put_select, put_textarea, pin, pin_wait_change
from pywebio import start_server

from centroid_util import centroid_main

import yaml

## LOADING USER INTERFACE DICT FROM YAML

yml_file = 'centroid_pars.yml'

with open(yml_file, "r") as file:
    in_pars = yaml.load(file, Loader=yaml.FullLoader)
    # Forming the variables for further use
    coord_format_help_md = in_pars['coord_format_help_md']
    coord_format_options = in_pars['coord_format']['options']
    in_pars.pop('coord_format_help_md') # delete unusable key otherwise it's error

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

if __name__ == '__main__':
    start_server(app, port=8080, debug=True)

