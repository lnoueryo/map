import os
from datetime import datetime as dt
import pandas as pd
from django.core.management.base import BaseCommand
from map.models import *
# from map.sqlite_models import *
from django.conf import settings

def execute(is_import):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    if is_import:
        import_data()

def import_data():
    os.path.join(settings.BASE_DIR / f'data/csv/stations.csv')
    df_companies = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/companies.csv')).fillna('')
    company_dict_list = df_companies.to_dict(orient='records')
    df_lines = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/lines.csv')).fillna('')
    line_dict_list = df_lines.to_dict(orient='records')
    df_stations = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/stations.csv')).fillna('')
    station_dict_list = df_stations.to_dict(orient='records')
    df_line_stations = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/line_stations.csv')).fillna('')
    line_stations_dict_list = df_line_stations.to_dict(orient='records')

    for company_dict in company_dict_list:
        tdatetime = dt.strptime(company_dict['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
        company_dict['created_at'] = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
        tdatetime = dt.strptime(company_dict['updated_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
        company_dict['updated_at'] = tdatetime.strftime('%Y-%m-%d %H:%M:%S')

    for line_dict in line_dict_list:
        tdatetime = dt.strptime(line_dict['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
        line_dict['created_at'] = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
        tdatetime = dt.strptime(line_dict['updated_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
        line_dict['updated_at'] = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
        line_dict['prefecture_id'] = '13'

    for station_dict in station_dict_list:
        station_dict['created_at'] = station_dict['created_at'].replace(' ', 'T') + ':00'
        tdatetime = dt.strptime(station_dict['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
        station_dict['created_at'] = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
        station_dict['updated_at'] = station_dict['updated_at'].replace(' ', 'T') + ':00'
        tdatetime = dt.strptime(station_dict['updated_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
        station_dict['updated_at'] = tdatetime.strftime('%Y-%m-%d %H:%M:%S')

    df_prefectures = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/prefectures.csv')).fillna('')
    prefecture_dict_list = df_prefectures.to_dict(orient='records')
    df_cities = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/cities.csv')).fillna('')
    city_dict_list = df_cities.to_dict(orient='records')
    df_facilities = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/city_facility.csv')).fillna(0)
    facility_dict_list = df_facilities.to_dict(orient='records')
    df_occupations = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/city_occupation.csv')).fillna('')
    occupation_dict_list = df_occupations.to_dict(orient='records')
    df_populations = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/city_population.csv')).fillna('')
    population_dict_list = df_populations.to_dict(orient='records')
    df_spots = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/spots.csv')).fillna('')
    spot_dict_list = df_spots.to_dict(orient='records')
    df_towns = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/towns.csv')).fillna(0)
    town_dict_list = df_towns.to_dict(orient='records')

    session.bulk_insert_mappings(Prefecture, prefecture_dict_list)
    for city_dict in city_dict_list:
        city_dict['id'] = city_dict['city_code']
    session.bulk_insert_mappings(City, city_dict_list)
    session.bulk_insert_mappings(Facility, facility_dict_list)
    session.bulk_insert_mappings(Occupation, occupation_dict_list)
    session.bulk_insert_mappings(Population, population_dict_list)
    session.bulk_insert_mappings(Spot, spot_dict_list)
    session.bulk_insert_mappings(Town, town_dict_list)
    session.bulk_insert_mappings(Company, company_dict_list)
    session.bulk_insert_mappings(Line, line_dict_list)
    session.bulk_insert_mappings(Station, station_dict_list)
    session.bulk_insert_mappings(LineStation, line_stations_dict_list)
    session.commit()
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--import', action='store_true')

    def handle(self, *args, **options):
        execute(options['import'])

