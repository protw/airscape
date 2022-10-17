# Yet another web app onto Docker

This is a pattern of the *Python*-based geo web app deployment onto *Docker* with the use of `pywebio`, `yaml`, `folium`, and `pygeodesy` packages. 

![docker-python](docker-python.png)

## Task description

> The essence of the actual task is not important in our consideration. It is formulated here for example. In the future, other tasks and solutions can be formed on the basis of this approach.

**Task**: A given text contains a description with a list of geolocations. The coordinates of these points can be written in text in different formats and have a different order of latitude and longitude (Lat, Long or Long, Lat). It is necessary to extract the coordinates of all points from the text, find their central point and display all points, including the central one, on the map on the web page. The application that generates this map must be portable, that is, not dependent on the operating system of the computer on which it is deployed. Also, this application should publish this map in the open space in the form of a web page.

## Code features

The main features of the app are:

- user interface and web service is based on the `pywebio` package;
- user interface is specified in a `yaml` file from which, data are converted into a *Python* dictionary;
- arguments for user interface functions are passed into using [unpacked dictionary mechanism](https://python-reference.readthedocs.io/en/latest/docs/operators/dict_unpack.html);
- creation of a map is based on the `folium` package;
- geodesic calculation is based on `pygeodesy` package.

## Files and their purpose

Here is given the complete list of files required for our solution:

- `centroid_calc_pywebio.py`– main script;
- `centroid_pars.yml` – specification of user interface elements;
- `centroid_util.py` – core geodesic calculation and map forming;
- `Dockerfile` – instructions for building the *Docker* image and running *Docker* container;
- `README.md` – description of the solution in English, there is also description in Ukrainian here `README-UKR.md`;
- `requirements.txt` – list of *Python* packages for building the *Docker* image.

## Brief code description

### Main script

Firstly, all necessary packages are imported:

```python
from pywebio.output import put_text, put_markdown, put_html, put_button, use_scope
from pywebio.pin import put_select, put_textarea, pin, pin_wait_change
from pywebio import start_server

from centroid_util import centroid_main

import yaml
```

Then the specification of user interface is loaded from the file `'centroid_pars.yml'` and converted to the dict `in_pars`:

```python
yml_file = 'centroid_pars.yml'

with open(yml_file, "r") as file:
    in_pars = yaml.load(file, Loader=yaml.FullLoader)
    # Forming the variables for further use
    coord_format_help_md = in_pars['coord_format_help_md']
    coord_format_options = in_pars['coord_format']['options']
    in_pars.pop('coord_format_help_md') # delete unusable key otherwise it's error
```

Important point here: all the keys in the dict correspond exactly to argument names of input methods. Thus corresponding values of the dict will be passed properly as argument values to input methods below.

Performing geo calculation, as well as forming the map and resulting text string is done by the function `disp_html`. This function is used as a callback in a button initiating the calculation and generation of the map.

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

 It is important to note that all the actions within this function regarding the rendering the results in the browser are performed in a particular scope provided by the method `use_scope` with the argument `clear` set `True` in order to refresh the scope each time when the method is called. 

The whole structure of web interface is shown in a simple yet effective way in the method `app` by means of `pywebio` methods:

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

Actually you can see three obvious parts here: the header, five input elements and the button launching the calculation and the result rendering. 

In the second block of this fragment the [unpacked dictionary mechanism](https://python-reference.readthedocs.io/en/latest/docs/operators/dict_unpack.html) is used for passing the actual argument values. When you explore the file `'centroid_pars.yml'` containing the specification of user interface elements you may notice five embedded dicts inside named as follow: `'coord_format'`, `'lat_lon_order'`, `'perctl'`, `'zoom_start'`, `'text'`. All the keys inside these five dicts are named in exact correspondence to arguments of the input methods used: `put_select`, `put_textarea`. 

### Specification of user interface elements

The file the `'centroid_pars.yml'` contains the specification of five user interface elements. Here you can see two of these five. YAML format is the most readable, therefore no explanation is needed (especially after reading the `pywebio` documentation):

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

### Core geodesic calculation and map forming

Core geodesic calculation and map forming is provided by code in `centroid_util.py`. Since this article describes issues of web app deployment, there is no point to deepen in explanation of this code. 

let us only note that there are only four methods inside:

- `parse_text` – it parses the input text - extract geo-coordinate pairs from the text and create a list of float-type coordinate pairs;
- `dist_stats` – it calculates some stats for distances from points to the central point;
- `show_pnts_on_map` – it builds points on the map with accompanying information;
- `centroid_main` – this method arranges all the methods in this file into logical order.

### Code Dockerization

Before you start dockerizing your applications, one way or another you will have to read at least a couple of popular articles on this topic. After reading them, the Dockerfile code presented below will be quite clear to you making extra letters redundant:

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

## App building and deployment

After all the described above, building and deploying our app in Docker is as simple as shown below.

Building a Docker image:

```bash
docker build --tag python-docker .
```

Run the image as container:

```bash
docker run -p 8080:8080 python-docker
```


Running the container in the browser on http://localhost:8080

## Final word

The presented code was completely tested and is workable.

So please enjoy: read, modify, experiment.

