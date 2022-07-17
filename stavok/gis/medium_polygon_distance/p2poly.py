import geojson
import folium
#from folium.features import DivIcon

polygon_file = 'data/open-polygon.geojson'
points_file = 'data/points.geojson'

with open(polygon_file) as f:
    data_poly = geojson.loads(f.read())
with open(points_file) as f:
    data_pnts = geojson.loads(f.read())

poi = data_pnts.features[0].geometry.coordinates[4]
poi = [poi[1], poi[0]] # in folium.Map the order is - Lat, Long
coord = data_pnts.features[0].geometry.coordinates

m = folium.Map(location=poi, zoom_start=9, tiles='cartodbpositron')
# Display polygon
folium.GeoJson(data_poly).add_to(m) # here the order is - Long, Lat

m.save('map_my_1.html')