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
    if file == 'all':
        company()
        city()
        city_detail()
    elif file == 'company':
        company()
    elif file == 'city':
        city()
    elif file == 'city_detail':
        city_detail()
    else:
        pass

def company():
    """
    client/assets/json/に設置されているcompany.jsonを読み込み
    companies, lines, stationsに分割してJSONのままで保存する。
    """
    file_path = os.path.join(settings.BASE_DIR / f'data/json/company.json')
    with open(file_path, mode='r',  encoding='utf-8') as f:
        companies = json.loads(f.read())
    json_file_path = os.path.join(settings.BASE_DIR / f'client/assets/json/company.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
            json.dump(companies, f, ensure_ascii=False, indent=2)

def city():
    """
    client/assets/json/に設置されているcompany.jsonを読み込み
    companies, lines, stationsに分割してJSONのままで保存する。
    """
    file_path = os.path.join(settings.BASE_DIR / f'data/json/city.json')
    with open(file_path, mode='r',  encoding='utf-8') as f:
        companies = json.loads(f.read())
    json_file_path = os.path.join(settings.BASE_DIR / f'client/assets/json/city.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
            json.dump(companies, f, ensure_ascii=False, indent=2)

def city_detail():
    """
    client/assets/json/に設置されているcompany.jsonを読み込み
    companies, lines, stationsに分割してJSONのままで保存する。
    """
    population_path = os.path.join(settings.BASE_DIR / f'data/json/city_population.json')
    with open(population_path, mode='r',  encoding='utf-8') as f:
        population = json.loads(f.read())

    occupation_path = os.path.join(settings.BASE_DIR / f'data/json/city_occupation.json')
    with open(occupation_path, mode='r',  encoding='utf-8') as f:
        occupation = json.loads(f.read())

    facility_path = os.path.join(settings.BASE_DIR / f'data/json/city_facility.json')
    with open(facility_path, mode='r',  encoding='utf-8') as f:
        facility = json.loads(f.read())

    json_population_path = os.path.join(settings.BASE_DIR / f'client/assets/json/city_population.json')
    with open(json_population_path, mode='w+', encoding='utf-8') as f:
        json.dump(population, f, ensure_ascii=False, indent=2)

    json_occupation_path = os.path.join(settings.BASE_DIR / f'client/assets/json/city_occupation.json')
    with open(json_occupation_path, mode='w+', encoding='utf-8') as f:
        json.dump(occupation, f, ensure_ascii=False, indent=2)

    json_facility_path = os.path.join(settings.BASE_DIR / f'client/assets/json/city_facility.json')
    with open(json_facility_path, mode='w+', encoding='utf-8') as f:
        json.dump(facility, f, ensure_ascii=False, indent=2)



class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file', nargs='?', default='all', type=str)

    def handle(self, *args, **options):
        execute(options['file'])