# Example how to render Holoviews plot at Spyder
# See: hv_spyder_rend.py

import holoviews as hv

hv.extension('bokeh')
xs = range(-10,11)
ys = [100-x**2 for x in xs]
curve = hv.Curve((xs, ys))

from hv_spyder_rend import hvshow

# The plot is shown when the line is run from command line! (?)
hvshow(curve,backend='bokeh')
