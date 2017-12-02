import json
import sys
from math import radians, cos, sin, asin, sqrt


def load_data(filepath):
    with open(filepath) as data:
        json_data = json.load(data)
    return json_data


def get_biggest_bar(bars_data):
    max_seats = 1
    max_seats_object = 0
    for bar in bars_data['features']:
        seats_count = bar['properties']['Attributes']['SeatsCount']
        if max_seats < seats_count:
            max_seats = seats_count
            max_seats_object = bar
    print(max_seats_object['properties']['Attributes']['Name'], max_seats_object['properties']['Attributes']['SeatsCount'])


def get_smallest_bar(bars_data):
    min_seats = 1
    min_seats_object = 0
    for bar in bars_data['features']:
        seats_count = bar['properties']['Attributes']['SeatsCount']
        if min_seats > seats_count:
            min_seats = seats_count
            min_seats_object = bar
    print(min_seats_object['properties']['Attributes']['Name'], min_seats_object['properties']['Attributes']['SeatsCount'])


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
    min_distance = 7000
    min_distance_object = None
    for bar in loaded_data['features']:
        bar_lon, bar_lat = bar['geometry']['coordinates']
        bar_distance = get_distance_in_km(user_lon, user_lat, bar_lon, bar_lat)
        # print(bar_distance)
        if min_distance > bar_distance:
            min_distance = bar_distance
            min_distance_object = bar
    return min_distance_object['properties']['Attributes']['Name']


if __name__ == '__main__':
    filepath = input("Please provide path to json: ")
    bars_data = load_data(filepath)
    get_biggest_bar(bars_data)
    get_smallest_bar(bars_data)
    user_lon, user_lat = input('\nPlease provide your lat long: ').split(" ")
    print('The closest bar is:', str(get_closest_bar(bars_data, float(user_lon), float(user_lat))))
