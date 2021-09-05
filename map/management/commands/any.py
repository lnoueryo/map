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
    new_city()

def new_city():
    df_cities = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/cities.csv'))
    cities_dict_list = id_to_str(df_cities.to_dict(orient='records'))
    df_spots = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/spots.csv'))
    spots_dict_list = id_to_str(df_spots.to_dict(orient='records'))

    for city in cities_dict_list:
        city['polygons'] = eval(city['polygons']) if 'polygons' in city and type(city['polygons']) == str else []
        del city['polygons']
        city['spots'] = [spot for spot in spots_dict_list if spot['city_code'] == city['city_code']]
        city['spots'] = [spot for spot in city['spots'] if city['name'] in spot['address']]
    spots = list(itertools.chain.from_iterable([[spot for spot in city['spots'] ] for city in cities_dict_list]))
    name_list = [spot['name'] for spot in spots]
    unique_spots = [spot for i, spot in enumerate(spots) if spot['name'] not in name_list[0:i]]
    for index, spot in enumerate(unique_spots):
        spot['id'] = index + 1

    df_spots = pd.DataFrame.from_dict(unique_spots, orient='columns')
    df_spots = df_spots.set_index('id')
    df_spots.to_csv(os.path.join(settings.BASE_DIR / f'data/csv/spots.csv'))

def id_to_str(spots):
    for spot in spots:
        spot['prefecture_id'] = str(spot['prefecture_id'])
        spot['city_code'] = str(spot['city_code'])
    return spots

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file', nargs='?', default='json', type=str)

    def handle(self, *args, **options):
        execute(options['file'])