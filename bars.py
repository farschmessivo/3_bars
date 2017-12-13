import json
import sys
from math import radians, cos, sin, asin, sqrt


def load_data(filepath):
    with open(filepath) as file:
        json_data = json.load(file)
    return json_data


def get_biggest_bar(bars):
    bar = max(bars, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])
    return bar


def get_smallest_bar(bars):
    bar = min(bars, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])
    return bar


def get_distance_in_km(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    from https://stackoverflow.com/a/4913653
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    radius_of_earth_in_km = 6371
    distance_in_km = radius_of_earth_in_km * c
    return distance_in_km


def get_bar_name(bar):
    return bar['properties']['Attributes']['Name']


def get_closest_bar(bars, user_lon, user_lat):
    bar = min(bars, key=lambda bar: get_distance_in_km(
        user_lon, user_lat, *bar['geometry']['coordinates']))
    return bar


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit("Usage: python3 bars.py <path_to_json>")
    filepath = sys.argv[1]
    bars_data = load_data(filepath)
    bars = bars_data['features']
    print('The biggest bar is:', get_bar_name(get_biggest_bar(bars)))
    print('The smallest bar is:', get_bar_name(get_smallest_bar(bars)))
    user_lon, user_lat = input('\nPlease provide your lat long: ').split(" ")
    print('The closest bar is:', get_bar_name(get_closest_bar(bars, float(user_lon), float(user_lat))))