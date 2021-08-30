# -*- coding: utf-8 -*-
import os
import json
import time
from datetime import datetime
import logging
import traceback
import itertools
from logging import Formatter, getLogger, FileHandler, DEBUG, ERROR

import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from pytz import timezone
from dateutil.relativedelta import relativedelta
import pandas as pd

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from gmap.geohash import Geohash


def execute(file):
    if file == 'json':
        create()
        new_city()
    elif file == 'csv':
        create_json()
        new_city_json()
    else:
        pass

def create():
    """
    client/assets/json/に設置されているcompany.jsonを読み込み
    companies, lines, stationsに分割してJSONのままで保存する。
    """
    df_cities = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/cities.csv'))
    cities_dict_list = parse_id_to_str(df_cities.to_dict(orient='records'))
    df_spots = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/spots.csv'))
    spots_dict_list = parse_id_to_str(df_spots.to_dict(orient='records'))

    for city in cities_dict_list:
        city['polygons'] = eval(city['polygons']) if 'polygons' in city and type(city['polygons']) == str else []
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/cities.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
            json.dump(cities_dict_list, f, ensure_ascii=False, indent=2)
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/spots.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
            json.dump(spots_dict_list, f, ensure_ascii=False, indent=2)

def new_city():
    df_cities = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/cities.csv'))
    cities_dict_list = parse_id_to_str(df_cities.to_dict(orient='records'))
    df_spots = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/spots.csv'))
    spots_dict_list = parse_id_to_str(df_spots.to_dict(orient='records'))

    for city in cities_dict_list:
        city['polygons'] = eval(city['polygons']) if 'polygons' in city and type(city['polygons']) == str else []
        city['spots'] = [spot for spot in spots_dict_list if spot['city_code'] == city['city_code']]
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/city.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
            json.dump(cities_dict_list, f, ensure_ascii=False, indent=2)

def parse_id_to_str(spots):
    for spot in spots:
        spot['prefecture_id'] = str(spot['prefecture_id'])
        spot['city_code'] = str(spot['city_code'])
    return spots

def change_spots():
    file_path = os.path.join(settings.BASE_DIR / f'client/assets/json/city.json')
    with open(file_path, mode='r',  encoding='utf-8') as f:
        cities = json.loads(f.read())
    for city in cities:
        for spot in city['spots']:
            spot['prefecture_id'] = '13'
            spot['city_code'] = city['city_code']
        del city['city']
    json_file_path = os.path.join(settings.BASE_DIR / f'client/assets/json/city.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
            json.dump(cities, f, ensure_ascii=False, indent=2)
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/cities.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
            json.dump(cities, f, ensure_ascii=False, indent=2)
    spots = list(itertools.chain.from_iterable([[spot for spot in word['spots']] for word in cities]))
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/spots.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
            json.dump(spots, f, ensure_ascii=False, indent=2)

def create_json():
    """
    client/assets/json/に設置されているcities.jsonを読み込み
    cities, spotsに分割してcsvに変換し保存する。
    """
    file_path = os.path.join(settings.BASE_DIR / f'data/json/city.json')
    with open(file_path, mode='r',  encoding='utf-8') as f:
        cities = json.loads(f.read())
        spots = list(itertools.chain.from_iterable([[spot for spot in word['spots']] for word in cities]))
    df_cities = pd.json_normalize(cities)
    df_cities = df_cities.drop('spots', axis=1)
    csv_file_path = os.path.join(settings.BASE_DIR / f'data/csv/cities.csv')
    df_cities.to_csv(csv_file_path, index=False, encoding='utf-8')
    df_spots = pd.json_normalize(spots)
    csv_file_path = os.path.join(settings.BASE_DIR / f'data/csv/spots.csv')
    df_spots.to_csv(csv_file_path, index=False, encoding='utf-8')

def new_city_json():
    file_path = os.path.join(settings.BASE_DIR / f'data/json/cities.json')
    with open(file_path, mode='r',  encoding='utf-8') as f:
        cities = json.loads(f.read())
    file_path = os.path.join(settings.BASE_DIR / f'data/json/spots.json')
    with open(file_path, mode='r',  encoding='utf-8') as f:
        spots = json.loads(f.read())
    for city in cities:
        city['spots'] = [spot for spot in spots if spot['city_code'] == city['city_code']]
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/city.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
            json.dump(cities, f, ensure_ascii=False, indent=2)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file', nargs='?', default='json', type=str)

    def handle(self, *args, **options):
        execute(options['file'])