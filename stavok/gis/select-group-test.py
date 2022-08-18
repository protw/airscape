import numpy as np
import folium
-from folium.plugins import HeatMap

lon, lat = -86.276, 30.935 
zoom_start = 5

data = (
    np.random.normal(size=(100, 3)) *
    np.array([[1, 1, 1]]) +
    np.array([[48, 5, 1]])
).tolist()
m = folium.Map([48, 5], tiles='stamentoner', zoom_start=6)

HeatMap(data).add_to(folium.FeatureGroup(name='Heat Map').add_to(m))
folium.LayerControl().add_to(m)

m.save("select-group-test.html")