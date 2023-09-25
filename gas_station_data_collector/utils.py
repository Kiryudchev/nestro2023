import re
import pandas as pd
import numpy as np
import json
import requests
from typing import List


def retrieve_bosnian_city(c):
    """Returns clean name of a town/village
    params:
    c: town name
    """
    c = ''.join(re.findall(r"[^\d]+", c)).strip()
    if ("Granica HR" in c) or ('Gr. BH/HR' in c) or ('Granica BH/HR' in c):
        left_bracket = c.find('(')
        right_bracket = c.find(')')
        c = c[left_bracket + 1:right_bracket]
        if '/' in c:
            c = ' and '.join(c.split('/'))
        if ';' in c:
            c = ' and '.join(c.split(';'))
    elif ('(' in c) and (')' in c):
        left_bracket = c.find('(')
        right_bracket = c.find(')')
        c = c[:left_bracket] + 'and ' + c[left_bracket + 1:right_bracket]

    return c


def retrieve_city_serb(c):
    """Returns clean name of a town/village
        params:
        c: town name
        """
    if not isinstance(c, str):
        return 'None'

    c = ''.join(re.findall(r"[^\d]+", c)).strip()

    if '-' in c:
        cs = [s.strip() for s in c.split('-')]
        for c in cs:
            if "granica" in c:
                left_bracket = c.find('(')
                right_bracket = c.find(')')
                c = c[left_bracket + 1:right_bracket]
                if '/' in c:
                    c = ' and '.join(c.split('/'))
                if ';' in c:
                    c = ' and '.join(c.split(';'))
            elif ('(' in c) and (')' in c):
                left_bracket = c.find('(')
                right_bracket = c.find(')')
                c = c[:left_bracket] + 'and ' + c[left_bracket + 1:right_bracket]
    else:
        if "granica" in c:
            left_bracket = c.find('(')
            right_bracket = c.find(')')
            c = c[left_bracket + 1:right_bracket]
            if '/' in c:
                c = ' and '.join(c.split('/'))
            if ';' in c:
                c = ' and '.join(c.split(';'))
        elif ('(' in c) and (')' in c):
            left_bracket = c.find('(')
            right_bracket = c.find(')')
            c = c[:left_bracket] + 'and ' + c[left_bracket + 1:right_bracket]

    return c


def format_code(code):
    """Formats highway codes to [Char Int] format
    """
    processed_codes = []

    if '/' in code:
        codes = code.split('/')
    else:
        codes = [code]

    if ';' in code:
        codes = code.split(';')
    else:
        codes = [code]

    for code in codes:
        if code:
            code = code.replace('-', ' ')
            if code[1] != ' ':
                code = code[0] + ' ' + code[1:]
            try:
                int(code[-1])
            except ValueError:
                code = code[:-1]

            processed_codes.append(code.strip())

    return processed_codes


def extract_fuel_stations(places):
    """
    Processes geo-spatial information of fuel stations location
    :param places: dictionaries with place geo information
    :return: list of dictionaries for each fuel station
    """
    cols = ['place_id', 'lat', 'lon', 'type', 'name', ['address', 'road'], ['address', 'state_district']]
    stations = []

    for place in places:
        fuel_station = {}
        for col in cols:
            if isinstance(col, list):
                if col[0] in place:
                    if col[1] in place[col[0]]:
                        fuel_station[col[1]] = place[col[0]][col[1]]
                    else:
                        fuel_station[col[1]] = 'None'
            else:
                if col in place:
                    fuel_station[col] = place[col]
                else:
                    fuel_station[col] = 'None'

        stations.append(fuel_station)

    return stations


def distribute_stations(processed_stations: List[dict], all_stations, station_ids):
    """
    Creates list of dictionaries with keys: highway codes, values: fuel station locations
    :param processed_stations: list of dictionaries processed by extract_fuel_stations func
    :param all_stations: dictionary with keys: highway codes, values: corresponding fuel stations
    :param station_ids: dictionary with keys: highway codes, values: fuel stations ids
    :return:
    """
    for fuelst in processed_stations:
        if 'road' in fuelst:
            if isinstance(fuelst['road'], str):
                roads = [fuelst['road']]
            else:
                roads = fuelst['road']

            for road in roads:
                road = road.replace('-', ' ')

                if 'place_id' in fuelst:
                    place_id = fuelst['place_id']
                    if road in station_ids:
                        if place_id in station_ids[road]:
                            continue
                        else:
                            station_ids[road].append(place_id)
                    else:
                        station_ids[road] = [place_id]

                if road != '' or road != 'None':
                    if road in all_stations:
                        all_stations[road].append(fuelst)
                    else:
                        all_stations[road] = [fuelst]

    return all_stations, station_ids


def get_codes_by_street(processed_stations, street_to_highway_codes):
    """
    Turns street names in geo-spatial descriptions of locations into corresponding highway codes
    :param processed_stations: list of dictionaries processed by extract_fuel_stations func
    :param street_to_highway_codes: dictionaty with keys: street names, values: highway codes
    :return: None
    """
    request_text_head = 'https://nominatim.openstreetmap.org/search?namedetails=1&street='
    request_text_tail = '&country=Bosna+i+Hercegovina&format=jsonv2'

    for item in processed_stations:
        if 'road' in item:
            if item['road'] in street_to_highway_codes:
                retrieved_codes = format_code(street_to_highway_codes[item['road']])
            else:
                request_core = '+'.join(item['road'].split())
                res = requests.get(request_text_head + request_core + request_text_tail).text
                jsoned = json.loads(res)
                road_code = ''

                for d in jsoned:
                    if 'ref' in d['namedetails']:
                        road_code = d['namedetails']['ref']
                        break
                    else:
                        continue

                street_to_highway_codes[item['road']] = road_code
                retrieved_codes = format_code(road_code)

            item['road'] = retrieved_codes

    return