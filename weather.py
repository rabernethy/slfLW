# weather.py
# Written by Russell Abernethy
# Date: 06/15/2021
# Desc: Takes a csv as input and outputs that csv with the added columns date and mean daily temperature.

import requests, csv
from sys import argv

filename, seen, lookup = argv[1], [], {}
fieldnames = ['Business Name', 'Full Address', 'Latitude', 'Longitude', 'Date', 'Mean Daily Temperature']

def call_api(gridId, gridX, gridY, i):
    maxitr = 4
    data = requests.get('https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast'.format(office = gridId, gridX = gridX, gridY = gridY)).json()
    try:
        return [data['properties']['updated'], (data['properties']['periods'][0]['temperature'] + data['properties']['periods'][1]['temperature']) / 2]
    except KeyError:
        if i < maxitr:
            call_api(gridId, gridX,gridY, i+1)
        else:
            print("Server error, Skipping Entry")
            return ["N/A","N/A"]

with open("weather+{}.cvs".format(filename[:-4]),"w", encoding='utf8') as output:
    writer = csv.DictWriter(output, fieldnames = fieldnames)
    writer.writeheader()
    with open(filename, "r", encoding = 'utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # For each entry in the input, find what grid it is in and then get the weather there.
            data = requests.get("https://api.weather.gov/points/{lat},{lon}".format(lat = row['Latitude'].strip(), lon = row['Longitude'].strip())).json()
            gridX = data['properties']['gridX']
            gridY = data['properties']['gridY']
            gridId = data['properties']['gridId']
            # Memoize the response if it has been seen before.
            if seen.count((gridX, gridY, gridId)) == 0:
                seen.append((gridX, gridY, gridId))
                r = requests.get('https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast'.format(office = gridId, gridX = gridX, gridY = gridY))
                data = r.json()
                weather = call_api(gridId, gridX, gridY, 0)
                lookup[str((gridX, gridY, gridId))] = weather
            else:
                date = lookup[str((gridX, gridY, gridId))][0]
                mdt = lookup[str((gridX, gridY, gridId))][1]
            writer.writerow({'Business Name': row['Business Name'], 'Full Address': row['Full Address'], 'Latitude': row['Latitude'], 'Longitude': row['Longitude'], 'Date': weather[0], 'Mean Daily Temperature': weather[1]})

