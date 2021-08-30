# -*- coding: utf-8 -*-
import os
import json
import time
from datetime import datetime
import logging
import traceback
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


formatter = Formatter('[%(levelname)s] %(asctime)s - %(message)s (%(filename)s)')
logger = getLogger(__name__)
handler = FileHandler(os.path.join(settings.BASE_DIR / f'log/geohash/log.txt'), encoding='utf-8')
handler.setLevel(DEBUG)
handler.setFormatter(formatter)

error_handler = FileHandler(os.path.join(settings.BASE_DIR / f'log/place_id/log.txt'), encoding='utf-8')
error_handler.setLevel(ERROR)
error_handler.setFormatter(formatter)

logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.addHandler(error_handler)

session = requests.Session()

retries = Retry(total=3,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])

session.mount('https://', HTTPAdapter(max_retries=retries))
session.mount('http://', HTTPAdapter(max_retries=retries))

def execute(file):
    if file == 'all':
        get_station_geohash()
        get_spot_geohash()
    elif file == 'station':
        get_station_geohash()
    elif file == 'spot':
        get_spot_geohash()
    else:
        pass
def get_station_geohash():
    df = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/stations.csv'), index_col=0)
    df['geohash'] = ''
    gh = Geohash()
    for i, row in df.iterrows():
        geohash = gh.encode(float(df.at[i, 'lat']), float(df.at[i, 'lng']), precision=7)
        df.at[i, 'geohash'] = geohash
    df.to_csv(os.path.join(settings.BASE_DIR / f'data/csv/stations.csv'))

def get_spot_geohash():
    df = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/spots.csv'), index_col=0)
    df['geohash'] = ''
    gh = Geohash()
    for i, row in df.iterrows():
        geohash = gh.encode(float(df.at[i, 'lat']), float(df.at[i, 'lng']), precision=7)
        df.at[i, 'geohash'] = geohash
    df.to_csv(os.path.join(settings.BASE_DIR / f'data/csv/spots.csv'))

def get_station_geohash_json():
    with open(os.path.join(settings.BASE_DIR / f'data/json/stations.json'), mode='r', encoding='utf-8') as f:
        dict_list = json.loads(f.read())
    no_geohash_stations = [station for station in dict_list if 'geohash' not in dict_list]
    if no_geohash_stations:
        gh = Geohash()
        for station in no_geohash_stations:
            geohash = gh.encode(float(station['lat']), float(station['lng']), precision=7)
            station['geohash'] = geohash
    with open(os.path.join(settings.BASE_DIR / f'data/json/stations.json'), mode='w+', encoding='utf-8') as f:
        json.dump(dict_list, f, ensure_ascii=False, indent=2)

def get_spot_geohash_json():
    with open(os.path.join(settings.BASE_DIR / f'data/json/spots.json'), mode='r', encoding='utf-8') as f:
        dict_list = json.loads(f.read())
    no_geohash_spots = [spot for spot in dict_list if 'geohash' not in dict_list]
    if no_geohash_spots:
        gh = Geohash()
        for spot in no_geohash_spots:
            geohash = gh.encode(float(spot['lat']), float(spot['lng']), precision=7)
            spot['geohash'] = geohash
    with open(os.path.join(settings.BASE_DIR / f'data/json/spots.json'), mode='w+', encoding='utf-8') as f:
        json.dump(dict_list, f, ensure_ascii=False, indent=2)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file', nargs='?', default='all', type=str)

    def handle(self, *args, **options):
        execute(options['file'])