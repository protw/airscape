# Task: to find closest point and corresponding distance from point (or several
# points) to polygon by using 'nearestOn3' method from PyGeodesy package:
# https://mrjean1.github.io/PyGeodesy/docs/pygeodesy.sphericalTrigonometry-module.html#nearestOn3

# Debugger in Spyder 5.1.5 does not work properly with python 3.9+.
# So, preliminary we have to solve problem of debugging in Spyder:
# > conda create -n gis -c conda-forge python=3.8.10 spyder=5.1.5 folium \
#   geojson geopy
# > activate gis
# > pip install PyGeodesy

from pygeodesy import sphericalTrigonometry as st

import geojson
import folium
from folium.features import DivIcon

## Read data
polygon_file = 'data/open-polygon.geojson'
points_file = 'data/points.geojson'

with open(polygon_file) as f:
    data_poly = geojson.loads(f.read())
with open(points_file) as f:
    data_pnts = geojson.loads(f.read())

## Transforming data for 'nearestOn3' method
def transform_data(data):
    # swap order of coords from [Long,Lat] to [Lat,Long]
    pnts = [[p[1],p[0]] for p in data.features[0].geometry.coordinates]
    # prepare data type appropriate for 'nearestOn3' method
    pnts_LL = [st.LatLon(p[0],p[1]) for p in pnts]
    return pnts, pnts_LL

pnts, pnts_LL = transform_data(data_pnts)
poly, poly_LL = transform_data(data_poly)

## Calculation of nearest points from reference point 'pnt_LL' to open 
## polygon 'poly_LL'
## 'nearest_pnts' == list of tuples (closest, distance, angle) where: 
##   -- 'closest' point as LatLon or LatLon3Tuple(lat, lon, height);
##   -- 'distance' is distance between 'closest' and the given point converted 
##      to meter, same units as 'radius' (by default);
##   -- 'angle' from the given point 'pnt_LL' to 'closest' in compass degrees.

nearest_pnts = [st.nearestOn3(pnt_LL, poly_LL) for pnt_LL in pnts_LL]
n_pnts = [[np[0].lat,np[0].lon] for np in nearest_pnts] 

#### DISPLAY RESULT

## Select middle point for displaying
poi = data_pnts.features[0].geometry.coordinates[4]
poi = [poi[1], poi[0]] # in folium.Map the order is - Lat, Long
poi_name = 'Middle point'

## Display polygon on the map
m = folium.Map(location=poi, zoom_start=9, tiles='openstreetmap')
folium.GeoJson(data_poly).add_to(m) # here the order is - Long, Lat

## Display reference points 'pnts' and nearest points 'n_pnts'
def show_pnts_on_map(points,map,color='red'):
    fstr = '<div style="font-size: 16pt; color: ' + color + '">{}</div>'
    for i,_ in enumerate(points):
        folium.CircleMarker(location=points[i], color=color, radius=5, 
                            fill=color).add_to(map)
        folium.map.Marker(location=points[i], 
                          icon=DivIcon(icon_size=(150, 36),icon_anchor=(0, 0),
                                       html=fstr.format(str(i+1))
        )).add_to(map)
    return map

m = show_pnts_on_map(pnts,m,'red')
m = show_pnts_on_map(n_pnts,m,'blue')

## Display line segments connecting reference points and corresponding 
## nearest points
for i,_ in enumerate(pnts):
    folium.PolyLine(locations=[pnts[i],n_pnts[i]], color='red').add_to(m)
    print(pnts[i][0], pnts[i][1], n_pnts[i][0], n_pnts[i][1],
          nearest_pnts[i][1],nearest_pnts[i][2])

## Store the map on the disk
m.save('map_my_1.html')

