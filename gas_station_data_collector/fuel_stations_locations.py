import json
import requests
from utils import extract_fuel_stations, get_codes_by_street, distribute_stations

all_stations = {}
stations_ids = {}

if __name__ == '__main__':

    with open('all_highways.json', 'r', encoding='utf-8') as f:
        all_highways = json.loads(f.read())

    all_highways = all_highways['codes']

    with open('street_to_highway_codes.json', 'r', encoding='utf-8') as f:
        street_to_highway_codes = json.loads(f.read())

    request_text_head = 'https://nominatim.openstreetmap.org/search?addressdetails=1&q=fuel+stations+near+'
    request_text_tail = '+bosnia+i+herzegovina&format=jsonv2'

    for code in all_highways:
        request_core = '+'.join(code.split())
        res = requests.get(request_text_head + request_core + request_text_tail).text
        jsoned = json.loads(res)

        processed_stations = extract_fuel_stations(jsoned)
        get_codes_by_street(processed_stations, street_to_highway_codes)
        all_stations, stations_ids = distribute_stations(processed_stations, all_stations, stations_ids)

    with open('all_stations.json', 'w') as f:
        json.dump(all_stations, f)

    with open('station_ids.json', 'w') as f:
        json.dump(stations_ids, f)