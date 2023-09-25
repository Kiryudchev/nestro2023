import json
import requests

if __name__ == '__main__':

    with open('primary_roads.json', 'r', encoding='utf-8') as f:
        primary_roads = json.loads(f.read())

    request_text_head = 'https://nominatim.openstreetmap.org/search?namedetails=1&street='
    request_text_tail = '&country=Bosna+i+Hercegovina&format=jsonv2'
    request_core = '1.+Drinske+brigade'

    street_to_highway_code = {}

    for name in primary_roads['primary_roads']:
        request_core = '+'.join(name.split())
        res = requests.get(request_text_head + request_core + request_text_tail).text
        jsoned = json.loads(res)
        road_name = ''

        for d in jsoned:
            if 'ref' in d['namedetails']:
                road_name = d['namedetails']['ref']
                break
            else:
                continue

        street_to_highway_code[name] = road_name

        d = {'highway_codes': street_to_highway_code}

    with open('street_to_highway_codes.json', 'w') as f:
        json.dump(street_to_highway_code, f)