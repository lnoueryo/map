import os
from bs4 import BeautifulSoup
import re
import pandas as pd
import json

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

def execute():
    drop_columns()
    city_population()
    city_occupation()
    city_facility()
    create_json()

def city_population():

    df = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/city_detail.csv'), index_col=0)
    df = df[[
        'name',
        'population',
        'japanese_population',
        'foreign_population',
        'basic_resident_register_population',
        'population_under_15',
        'population_between_15_64',
        'population_over_65',
        'daytime_population',
        'births',
        'death',
        'total_households',
        'households',
        'nuclear_family_households',
        'single_households',
        'transferees',
        'mover',
        'marriages',
        'divorces',
        'area',
        'resident_area',
    ]]
    df_new = df.rename(
        columns={
            'japanese_population': 'japanese',
            'foreign_population': 'foreign',
            'population_under_15': 'under15',
            'population_between_15_64': 'between15_64',
            'population_over_65': 'over65',
            'daytime_population': 'daytime'
        }
    )
    df_new.to_csv(os.path.join(settings.BASE_DIR / f'data/csv/city_population.csv'))

def city_occupation():

    df = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/city_detail.csv'), index_col=0)
    df = df[[
        'name',
        'taxpayers',
        'offices',
        'kindergartener',
        'elementary_school_teacher',
        'elementary_school_student',
        'junior_high_school_teacher',
        'junior_high_school_student',
        'high_school_student',
        'working_age_population',
        'employed_population',
        'unemployed_population',
        'employed_population',
        'executive_officer',
        'owners',
        'self_employed',
        'family_employees',
        'workers_in_your_city',
        'workers_in_another_city',
        'employees_working_in_office',
        'commuting_population_from_other_city',
        'doctor',
        'dentist',
        'pharmacist'
    ]]
    df.to_csv(os.path.join(settings.BASE_DIR / f'data/csv/city_occupation.csv'))

def city_facility():

    df = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/city_detail.csv'), index_col=0)
    df = df[[
        'name',
        'community_center',
        'library',
        'house',
        'occupation_area',
        'total_waste_discharge',
        'garbage_recycling_rate',
        'shop',
        'restaurant',
        'store',
        'supermarket',
        'hospital',
        'clinic',
        'dental_clinic',
        'nursing_facility',
        'orphanage',
        'nursery_center',
        'kindergarten',
        'elementary_school',
        'junior_high_school',
        'high_school',
    ]]
    df.to_csv(os.path.join(settings.BASE_DIR / f'data/csv/city_facility.csv'))

def create_json():
    df_population = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/city_population.csv'))
    df_occupation = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/city_occupation.csv'))
    df_facility = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/city_facility.csv'))

    poplation_dict_list = df_population.to_dict(orient='records')
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/city_population.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
        json.dump(code_to_str(poplation_dict_list), f, ensure_ascii=False, indent=2)

    occupation_dict_list = df_occupation.to_dict(orient='records')
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/city_occupation.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
        json.dump(code_to_str(occupation_dict_list), f, ensure_ascii=False, indent=2)

    facility_dict_list = df_facility.to_dict(orient='records')
    json_file_path = os.path.join(settings.BASE_DIR / f'data/json/city_facility.json')
    with open(json_file_path, mode='w+', encoding='utf-8') as f:
        json.dump(code_to_str(facility_dict_list), f, ensure_ascii=False, indent=2)

def drop_columns():

    df = pd.read_csv(os.path.join(settings.BASE_DIR / f'data/csv/original_life.csv'), index_col=0)
    df = df.drop([
        'densely_inhabited_district_population',
        'nuclear_family_households_with_over_65',
        'elderly_households',
        'elderly_single_households',
        'taxable_income',
        'secondary_industry_establishments',
        'real_debt_service_ratio',
        'total_government_revenue',
        'total_government_spending',
        'local_tax',
        'primary_industry_employment',
        'secondary_industry_employment',
        'tertiary_industry_employment',
        'owner_occupied_house',
        'rented_house',
        'population_not_connected_to_sewage_lines',
        'planned_collection_population',
        'insured',
    ], axis=1)
    df = df.drop(index=[13, 13100], axis=0)
    df.to_csv(os.path.join(settings.BASE_DIR / f'data/csv/city_detail.csv'))

def code_to_str(dict_list):
    for dict in dict_list:
        dict['city_code'] = str(dict['city_code'])
    return dict_list

def create_city_detail():
    with open('./life.tsv', mode='r', encoding='utf-8') as f:
        city_detail = f.read()
        city_detail = city_detail.replace(',', '')
        city_detail = city_detail.replace('\t', ',')
    with open('./life.csv', mode='w+', encoding='utf-8') as f:
        f.write(city_detail)

def concat():
    df_summery1 = pd.read_csv('./summery1.tsv', index_col=0, sep='\t')
    df_summery2 = pd.read_csv('./summery2.tsv', index_col=0, sep='\t')
    df_summery2 = df_summery2.drop(['市区町村', 'Municipalities'], axis=1)
    df_new_summery = pd.concat([df_summery1, df_summery2], axis=1)
    df_new_summery.to_csv('./life.tsv', sep='\t')

def csv_to_json():
    df = pd.read_csv('./life.csv')
    # df.to_csv('./life.csv')
    dict_list = df.to_dict(orient='records')
    with open('./life.json', mode='w+', encoding='utf-8') as f:
            json.dump(dict_list, f, ensure_ascii=False, indent=2)


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument('file', nargs='?', default='all', type=str)

    def handle(self, *args, **options):
        execute()