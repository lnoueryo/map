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
import numpy as np

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from gmap.geohash import Geohash


def execute(file):
    if file == 'json':
        create()
        join_table()
        new_companies()
    elif file == 'csv':
        create_json()
        new_companies_json()
    else:
        pass

def create():
    """
    data/csv/に設置されているcompanies.csv, lines.csv, stations.csvを読み込み
    JSONに変換し保存。
    csv to json
    """
    df_companies = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/companies.csv'))
    companies_dict_list = df_companies.to_dict(orient='records')
    df_lines = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/lines.csv'))
    lines_dict_list = df_lines.to_dict(orient='records')
    df_stations = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/stations.csv'))
    stations_dict_list = id_to_str(df_stations.to_dict(orient='records'))
    for line in lines_dict_list:
        line['polygon'] = eval(line['polygon'])
    with open(os.path.join(settings.BASE_DIR / f'data/json/companies.json'), mode='w+', encoding='utf-8') as f:
        json.dump(companies_dict_list, f, ensure_ascii=False, indent=2)
    with open(os.path.join(settings.BASE_DIR / f'data/json/lines.json'), mode='w+', encoding='utf-8') as f:
        json.dump(lines_dict_list, f, ensure_ascii=False, indent=2)
    with open(os.path.join(settings.BASE_DIR / f'data/json/stations.json'), mode='w+', encoding='utf-8') as f:
        json.dump(stations_dict_list, f, ensure_ascii=False, indent=2)

def join_table():
    """
    data/csv/に設置されているline_stations.csvを読み込み
    JSONに変換して保存する。
    """
    file_path = os.path.join(settings.BASE_DIR / f'data/csv/line_stations.csv')
    df = pd.read_csv(file_path)
    dict_list = df.to_dict(orient='records')
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/line_stations.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
            json.dump(dict_list, f, ensure_ascii=False, indent=2)

def new_companies():
    """
    companies.csv, lines.csv, line_stations.csv, stations.csv
    を読み込みcompany.jsonを作成
    """
    df_companies = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/companies.csv'))
    companies = df_companies.to_dict(orient='records')
    lines = combine_through_line_jointable()

    for company in companies:
        company['lines'] = [line for line in lines if company['id'] == line['company_id']]
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/company.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
        json.dump(companies, f, ensure_ascii=False, indent=2)

def combine_through_line_jointable():
    df_lines = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/lines.csv'))
    lines = df_lines.to_dict(orient='records')
    df_line_stations = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/line_stations.csv'))
    line_stations = df_line_stations.to_dict(orient='records')
    df_stations = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/stations.csv'))
    stations = df_stations.to_dict(orient='records')

    for line in lines:
        line['polygon'] = eval(line['polygon'])
        line_station_list = [line_station for line_station in line_stations if line['id'] == line_station['line_id']]
        station_list = [station for station in id_to_str(stations) for line_station in line_station_list if line_station['station_id'] == station['id']]
        line['stations'] = station_list
    return lines

def change_station():
    """
    client/assets/json/に設置されているcompany.jsonを読み込み
    stationsに変更を加える。
    """
    file_path = os.path.join(settings.BASE_DIR / f'data/json/company.json')
    with open(file_path, mode='r',  encoding='utf-8') as f:
        companies = json.loads(f.read())
    for company in companies:
        for line in company['lines']:
            for station in line['stations']:
                # 変更および追加
                station['name'] = station['name'] + '駅'
                station['lat'] = float(station['lat'])
                station['lng'] = float(station['lng'])
        lines = list(itertools.chain.from_iterable([[line for line in company['lines']] for company in companies]))
        stations = list(itertools.chain.from_iterable([[station for station in line['stations']] for line in lines]))
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/stations.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
            json.dump(stations, f, ensure_ascii=False, indent=2)

def id_to_str(stations):
    for station in stations:
        station['prefecture_id'] = str(station['prefecture_id'])
        station['city_code'] = str(station['city_code'])
        if not type(station['place_ids']) == str and np.isnan(float(station['place_ids'])):
            station['place_ids'] = ''
    return stations


def create_json():
    """
    client/assets/json/に設置されているcompany.jsonを読み込み
    companies, lines, stationsに分割してcsvに変換し保存する。
    json to csv
    """
    file_path = os.path.join(settings.BASE_DIR / f'data/json/company.json')
    # file_path = os.path.join(settings.BASE_DIR / f'client/assets/json/company.json')
    with open(file_path, mode='r',  encoding='utf-8') as f:
        companies = json.loads(f.read())
        lines = list(itertools.chain.from_iterable([[line for line in company['lines']] for company in companies]))
        stations = list(itertools.chain.from_iterable([[station for station in line['stations']] for line in lines]))

    df_companies = pd.json_normalize(companies)
    df_companies = df_companies.drop('lines', axis=1)
    csv_file_path = os.path.join(settings.BASE_DIR / f'data/csv/companies.csv')
    df_companies.to_csv(csv_file_path, index=False, encoding='utf-8')

    for line in lines:
        line['polygon'] = str(line['polygon'])
    df_lines = pd.json_normalize(lines)
    df_lines = df_lines.drop('stations', axis=1)
    csv_file_path = os.path.join(settings.BASE_DIR / f'data/csv/lines.csv')
    df_lines.to_csv(csv_file_path, index=False, encoding='utf-8')

    df_stations = pd.json_normalize(stations)
    df_stations = df_stations.drop_duplicates()
    csv_file_path = os.path.join(settings.BASE_DIR / f'data/csv/stations.csv')
    df_stations.to_csv(csv_file_path, index=False, encoding='utf-8')

def new_companies_json():
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/companies.json')
    with open(json_file_path, mode='r',  encoding='utf-8') as f:
        companies = json.loads(f.read())
    lines = combine_through_line_jointable_json()

    for company in companies:
        company['lines'] = [line for line in lines if company['id'] == line['company_id']]
    df_companies = pd.json_normalize(companies)
    csv_file_path = os.path.join(settings.BASE_DIR / f'data/csv/company.tsv')
    df_companies.to_csv(csv_file_path, index=False, encoding='utf-8', sep='\t')
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/company.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
        json.dump(companies, f, ensure_ascii=False, indent=2)

def combine_through_line_jointable_json():
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/lines.json')
    with open(json_file_path, mode='r',  encoding='utf-8') as f:
        lines = json.loads(f.read())
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/line_stations.json')
    with open(json_file_path, mode='r',  encoding='utf-8') as f:
        line_stations = json.loads(f.read())
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/stations.json')
    with open(json_file_path, mode='r',  encoding='utf-8') as f:
        stations = json.loads(f.read())
    for line in lines:
        line_station_list = [line_station for line_station in line_stations if line['id'] == line_station['line_id']]
        station_list = [station for station in stations for line_station in line_station_list if line_station['station_id'] == station['id']]
        line['stations'] = station_list
    return lines

def join_table_from_json():
    """
    client/assets/json/に設置されているcompany.jsonを読み込み
    lines, stationsの中間テーブルデータを作成し、JSONで保存する。
    """
    file_path = os.path.join(settings.BASE_DIR / f'client/assets/json/company.json')
    with open(file_path, mode='r',  encoding='utf-8') as f:
        companies = json.loads(f.read())
        lines = list(itertools.chain.from_iterable([[line for line in company['lines']] for company in companies]))
        stations = [[station['id'] for station in line['stations']] for line in lines]
        line_stations = []
        id = 1
        for line, station in zip(lines, stations):
            for station_id in station:
                line_station = {
                    'id': id,
                    'line_id': line['id'],
                    'station_id': station_id
                }
                line_stations.append(line_station)
                id += 1
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/line_stations.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
            json.dump(line_stations, f, ensure_ascii=False, indent=2)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file', nargs='?', default='json', type=str)

    def handle(self, *args, **options):
        execute(options['file'])