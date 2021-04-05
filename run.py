import requests
import math
import json

import togeojsontiles
import geojson
import shapely.geometry
import shapely.ops

dir_name ='qs_ledger/apple_health/data/workout-routes'

def convert_to_geojson():
    for full_filename in os.listdir(dir_name):
        base = os.path.basename(full_filename)
        file = os.path.splitext(base)[0]
        togeojsontiles.gpx_to_geojson(file_gpx=f'{dir_name}/{full_filename}', file_geojson=f'{dir_name}/../geojson/{file}.geojson')

def create_geosjon(geo):
    return {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "allroutes"            
            },
            "geometry": geo
        }
    ]
    }

def merge_list(li):
    with open('all_routes.geojson') as geojson1:
        curr = json.load(geojson1)

    curr = shapely.geometry.asShape(poly1_geojson['features'][0]['geometry'])    
    for i in li[1:]:
        with open(i) as geojson2:
            poly2_geojson = json.load(geojson2)
        # pulling out the polygons
        poly2 = shapely.geometry.asShape(poly2_geojson['features'][0]['geometry'])        
        curr = curr.union(poly2)
    # using geojson module to convert from WKT back into GeoJSON format
    geojson_out = geojson.Feature(geometry=curr, properties={"name": "name"})
    allroutes = create_geosjon(geojson_out.geometry)

    # outputting the updated geojson file - for mapping/storage in its GCS format
    with open('all_routes.geojson', 'w') as outfile:
        json.dump(allroutes, outfile, indent=3 )

li = os.listdir(f'{dir_name}/../geojson/')
merge_list([f'{dir_name}/../geojson/{i}' for i in li[400:500]])

def check_overlap(file2):
    file1 =f'all_routes.geojson'
    with open(file1) as geojson1:
        poly1_geojson = json.load(geojson1)

    with open(file2) as geojson2:
        poly2_geojson = json.load(geojson2)

    # pulling out the polygons
    poly1 = shapely.geometry.asShape(poly1_geojson['features'][0]['geometry'])
    poly2 = shapely.geometry.asShape(poly2_geojson['features'][0]['geometry'])

    # checking to make sure they registered as polygons
    print(poly1.geom_type)
    print(poly2.geom_type)

    if poly1.intersects(poly2):
        overlap = poly1.intersection(poly2)
        print('overlap:', len(list(overlap)), ' ', file2)

    else: 
        print('no overlap')
    return overlap,poly2 
    
overlap,poly2  = check_overlap(f'{dir_name}/../geojson/{li[150]}')
overlap,poly2

user_token = 'insert_token_here'

def get_isochrone():
    """https://docs.mapbox.com/playground/isochrone/"""
    l_long = '10.7210255'
    l_lat = '59.921678'
    r = requests.get(f'https://api.mapbox.com/isochrone/v1/mapbox/walking/{l_long}%2C{l_lat}?contours_minutes=15%2C30%2C45%2C60&polygons=true&access_token={user_token}')

    outer_lines =  r.json()
    with open('Isochrone.json', 'w') as f:
        json.dump(outer_lines, f)
    return outer_lines

outer_lines = get_isochrone()
outer_geo_locations = outer_lines['features'][0]['geometry']['coordinates'][0]
striding_number = math.floor(len(outer_geo_locations)/3)
location_to_check = [v for i, v in enumerate(outer_geo_locations) if i % striding_number == 0]

def get_direction(to_long, to_lat, start_long='10.7210255', start_lat='59.921678'):
    fetch_dir_url = f'https://api.mapbox.com/directions/v5/mapbox/walking/{start_long}%2C{start_lat}%3B{to_long}%2C{to_lat}?alternatives=true&geometries=geojson&steps=false&access_token={user_token}'
    r = requests.get(fetch_dir_url)
    return r.json()

running_route = {'num':-1, "overlap": 10000 }
for num, loc in enumerate(location_to_check):
    d = get_direction(*loc)
    d = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": f'dir_{num}'            
            },
            "geometry": d['routes'][0]['geometry']
        }
    ]
    }

    with open(f'dir_{num}.json', 'w') as f:
        json.dump(d, f)

    overlap,poly2 = check_overlap(f'dir_{num}.json')

    if running_route['overlap'] > len(list(overlap)): 
        running_route = {'num':num, "overlap":len(list(overlap)), "pol": poly2 }

running_route
