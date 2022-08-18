import geopandas
from shapely.geometry import Polygon, Point
#from shapely.ops import nearest_points


poly = [
  (4.338074,50.848677), 
  (4.344961,50.833264), 
  (4.366227,50.840809), 
  (4.367945,50.852455), 
  (4.346693,50.858306)]
gpoly = geopandas.GeoSeries(Polygon(poly))
gpoly.set_crs("EPSG:4326")

pnt = [
  (4.382617,50.811948),
  ((poly[0][0]+poly[1][0])/2., (poly[0][1]+poly[1][1])/2.)]
gpnt = geopandas.GeoSeries([Point(pnt[0])])
gpnt.set_crs("EPSG:4326")

dist = gpoly.distance(gpnt)
print(dist)

#p1, p2 = nearest_points(gpoly, gpnt)