# weather.py
# Written by Russell Abernethy
# Date: 06/15/2021
# Desc: Takes a csv as input and outputs that csv with the added columns date and mean daily temperature.

import requests, csv
from sys import argv

filename, seen, lookup = argv[1], [], {}
fieldnames = ['Latitude','Longitude','Date Refreshed','MDT_0', 'MDT_1', 'MDT_2',  'MDT_3', 'MDT_4', 'MDT_5', 'MDT_6']

def call_api(gridId, gridX, gridY, i):
    maxitr = 3
    data = requests.get('https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast'.format(office = gridId, gridX = gridX, gridY = gridY)).json()
    try:
        return [data['properties']['updated'], (data['properties']['periods'][0]['temperature'] + data['properties']['periods'][1]['temperature'])/2, (data['properties']['periods'][2]['temperature'] + data['properties']['periods'][3]['temperature'])/2, (data['properties']['periods'][4]['temperature'] + data['properties']['periods'][5]['temperature'])/2, (data['properties']['periods'][6]['temperature'] + data['properties']['periods'][7]['temperature'])/2, (data['properties']['periods'][8]['temperature'] + data['properties']['periods'][9]['temperature'])/2, (data['properties']['periods'][10]['temperature'] + data['properties']['periods'][11]['temperature'])/2,  (data['properties']['periods'][12]['temperature'] + data['properties']['periods'][13]['temperature'])/2]
    except KeyError:
        if i < maxitr:
            return call_api(gridId, gridX,gridY, i+1)
        else:
            print("Server error, Skipping Entry")
            return ["Error", "Error", "Error", "Error", "Error", "Error", "Error", "Error"]

with open("weather+{}.csv".format(filename[:-4]),"w", encoding='utf8') as output:
    writer = csv.DictWriter(output, fieldnames = fieldnames)
    writer.writeheader()
    with open(filename, "r", encoding = 'utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print("Entry: {} - {} - {}".format(row['Business Name'],row['Latitude'],row['Longitude']))
            # For each entry in the input, find what grid it is in and then get the weather there.
            data = requests.get("https://api.weather.gov/points/{lat},{lon}".format(lat = row['Latitude'].strip(), lon = row['Longitude'].strip())).json()
            gridX = data['properties']['gridX']
            gridY = data['properties']['gridY']
            gridId = data['properties']['gridId']
            # Memoize the response if it has been seen before.
            if seen.count((gridX, gridY, gridId)) == 0:
                seen.append((gridX, gridY, gridId))
                weather = call_api(gridId, gridX, gridY, 0)
                lookup[str((gridX, gridY, gridId))] = weather
            else:
                weather = lookup[str((gridX, gridY, gridId))]
            writer.writerow({'Latitude': row['Latitude'], 'Longitude': row['Longitude'], 'Date Refreshed': weather[0], 'MDT_0': weather[1], "MDT_1": weather[2], 'MDT_2': weather[3], 'MDT_3': weather[4], "MDT_4": weather[5], 'MDT_5': weather[6], 'MDT_6': weather[7]})

