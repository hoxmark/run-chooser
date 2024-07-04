import datetime
import os
from math import atan2, cos, radians, sin, sqrt

import folium
import gpxpy
import gpxpy.gpx
from folium.plugins import HeatMap


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lat2 - lon2)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def import_gpx_files(directory):
    gpx_files = [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.endswith(".gpx")
    ]
    routes = []
    for gpx_file in gpx_files:
        with open(gpx_file, "r") as f:
            gpx = gpxpy.parse(f)
            for track in gpx.tracks:
                for segment in track.segments:
                    route = [
                        (point.latitude, point.longitude, point.elevation, point.time)
                        for point in segment.points
                    ]
                    routes.append(route)
    return routes


def calculate_distances_and_elevation(routes):
    distances, elevations = [], []
    for route in routes:
        total_distance, total_elevation_gain = 0.0, 0.0
        for i in range(1, len(route)):
            lat1, lon1, lat2, lon2 = (
                route[i - 1][0],
                route[i - 1][1],
                route[i][0],
                route[i][1],
            )
            total_distance += haversine(lat1, lon1, lat2, lon2)
            elevation_gain = route[i][2] - route[i - 1][2]
            if elevation_gain > 0:
                total_elevation_gain += elevation_gain
        distances.append(total_distance)
        elevations.append(total_elevation_gain)
    return distances, elevations


def calculate_pace(route):
    total_time = (route[-1][3] - route[0][3]).total_seconds() / 60
    total_distance = sum(
        haversine(route[i - 1][0], route[i - 1][1], route[i][0], route[i][1])
        for i in range(1, len(route))
    )
    return total_time / total_distance if total_distance > 0 else 0


def categorize_by_season(date):
    Y = 2000  # Dummy year for consistent datetime comparisons
    seasons = {
        "spring": (datetime.date(Y, 3, 21), datetime.date(Y, 6, 20)),
        "summer": (datetime.date(Y, 6, 21), datetime.date(Y, 9, 22)),
        "fall": (datetime.date(Y, 9, 23), datetime.date(Y, 12, 20)),
        "winter": (datetime.date(Y, 12, 21), datetime.date(Y, 3, 20)),
    }
    date = date.replace(year=Y)
    for season, (start, end) in seasons.items():
        if start <= date <= end:
            return season
    return "winter"


def seasonal_analysis(routes, distances):
    seasons = {"spring": [], "summer": [], "fall": [], "winter": []}
    for route, distance in zip(routes, distances):
        season = categorize_by_season(route[0][3].date())
        pace = calculate_pace(route)
        seasons[season].append((distance, pace))
    season_data = {
        season: (
            {
                "total_distance": sum(d[0] for d in data),
                "avg_pace": sum(d[1] for d in data) / len(data),
            }
            if data
            else {"total_distance": 0, "avg_pace": 0}
        )
        for season, data in seasons.items()
    }
    return season_data


def create_heatmap(routes):
    start_location = routes[0][0][:2] if routes else [0, 0]
    m = folium.Map(location=start_location, zoom_start=13, tiles="CartoDB dark_matter")
    heat_data = [point[:2] for route in routes for point in route]
    HeatMap(heat_data).add_to(m)
    return m
