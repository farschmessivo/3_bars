import json
import sys
from math import radians, cos, sin, asin, sqrt


def load_data(filepath):
    with open(filepath) as data:
        json_data = json.load(data)
    return json_data


def get_biggest_bar(bars_data):
    bars = bars_data['features']
    bar = max(bars, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])
    return bar['properties']['Attributes']['Name'], bar['properties']['Attributes']['SeatsCount']


def get_smallest_bar(bars_data):
    bars = bars_data['features']
    bar = min(bars, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])
    return bar['properties']['Attributes']['Name'], bar['properties']['Attributes']['SeatsCount']


def get_distance_in_km(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    distance_in_km = 6371 * c
    return distance_in_km


def get_closest_bar(loaded_data, user_lon, user_lat):
    bars = bars_data['features']
    bar = min(bars, key=lambda bar: get_distance_in_km(
        user_lon, user_lat, *bar['geometry']['coordinates']))
    return bar['properties']['Attributes']['Name']


if __name__ == '__main__':
    filepath = input("Please provide path to json: ")
    bars_data = load_data(filepath)
    # get_biggest_bar(bars_data)
    # get_smallest_bar(bars_data)
    print('The biggest bar is:', get_biggest_bar(bars_data))
    print('The smallest bar is:', get_smallest_bar(bars_data))
    user_lon, user_lat = input('\nPlease provide your lat long: ').split(" ")
    print('The closest bar is:', str(get_closest_bar(bars_data, float(user_lon), float(user_lat))))