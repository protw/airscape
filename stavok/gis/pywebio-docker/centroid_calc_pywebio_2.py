# -*- coding: utf-8 -*-

## IMPORT OF MODULES

from pywebio.output import put_text, put_markdown, put_html, put_button, use_scope, put_row
from pywebio.pin import put_select, put_textarea, pin, pin_wait_change

from pywebio.platform.flask import webio_view
#from pywebio.platform.flask import wsgi_app
from pywebio import start_server
#from pywebio.platform.flask import start_server
from flask import Flask
#from pywebio.platform.tornado_http import start_server

from centroid_util import centroid_main

import yaml

## LOADING USER INTERFACE DICT FROM YAML

yml_file = 'centroid_pars.yml'

with open(yml_file, "r") as file:
    in_pars = yaml.load(file, Loader=yaml.FullLoader)

# Forming the variables for further use
coord_format_help_md = in_pars['coord_format_help_md']
coord_format_options = in_pars['coord_format']['options']

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

def main():
    # Display header
    put_markdown('# ВХІДНІ ПАРАМЕТРИ 3')

    # Render input elements, input arguments are passed via 
    # unpacked dict instead of plain list
    put_row(
        [ put_select(**in_pars['coord_format']),
          None,
          put_select(**in_pars['perctl']) ], 
        size='50% 10px 50%')
    put_row(
        [ put_select(**in_pars['lat_lon_order']),
          None,
          put_select(**in_pars['zoom_start']) ], 
        size='50% 10px 50%')
    put_row(
        [ put_textarea(**in_pars['text']), 
          None, 
          put_markdown(coord_format_help_md)], 
        size='40% 10px 60%')
    
    # Launch calculation, display map and text result
    put_button('РАХУВАТИ', onclick=lambda: disp_html())

app = Flask(__name__)

# `task_func` is PyWebIO task function
app.add_url_rule('/', 'webio_view', webio_view(main),
            methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods
            #methods=['POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods

if __name__ == '__main__':
    #webio_view(app)
    #wsgi_app(app)
    #start_server(app, port=8080, debug=True)
    app.run(host='localhost', port=8080)

