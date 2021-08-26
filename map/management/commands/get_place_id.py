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

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from gmap.geohash import Geohash
# from map.models import Point

formatter = Formatter('[%(levelname)s] %(asctime)s - %(message)s (%(filename)s)')
logger = getLogger(__name__)
handler = FileHandler('./url_log/log.txt', encoding='utf-8')
handler.setLevel(DEBUG)
handler.setFormatter(formatter)

error_handler = FileHandler('./url_log/error.txt', encoding='utf-8')
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
# logger = logging.getLogger('server.cron')

def execute():
    read_words()
#     try:
#         points = Point.objects.filter(map_id=map_id)
#         now = datetime.now(timezone('Asia/Tokyo'))
#         for point in points:
#                 extra_fields_dict = json.loads(point.extra_fields)
#                 search_word = point.address + '' + point.name

#                 # extra_fieldsのカラムにplaces_idがない初めての取得の場合
#                 if 'places_id' not in extra_fields_dict:

#                     # extra_fieldsにplaces_date, places_result, places_id, places_queryキーを作成
#                     extra_fields_dict['places_id'] = ''
#                     extra_fields_dict['places_result'] = 0
#                     extra_fields_dict['places_date'] = ''
#                     extra_fields_dict['places_query'] = ''

#                     extra_fields_dict = get_place_id(extra_fields_dict, search_word, point)
#                     point.extra_fields = json.dumps(extra_fields_dict, ensure_ascii=False)
#                     print(point.key)
#                     time.sleep(1)
#                     continue

#                 # 住所＋名前が変更されている場合
#                 if not extra_fields_dict['places_query'] == search_word:
#                     extra_fields_dict = get_place_id(extra_fields_dict, search_word, point)
#                     point.extra_fields = json.dumps(extra_fields_dict, ensure_ascii=False)
#                     print(point.key)
#                     time.sleep(1)
#                     continue

#                 places_date = datetime.strptime(extra_fields_dict['places_date'], '%Y-%m-%dT%H:%M:%S.%f%z')
#                 one_year_later = places_date + relativedelta(years=+1)

#                 # 最後に取得した日にちが1年を過ぎた場合
#                 if one_year_later < now:
#                     extra_fields_dict = get_place_id(extra_fields_dict, search_word, point)
#                     point.extra_fields = json.dumps(extra_fields_dict, ensure_ascii=False)
#                     print(point.key)
#                     time.sleep(1)
#         Point.objects.bulk_update(points, ['extra_fields'])
#     except Exception:
#         logger.log(logging.ERROR, traceback.format_exc())
#         print(traceback.format_exc())

def get_place_id(extra_fields_dict, search_word, point):
    try:
        payload = {'input': search_word, 'inputtype': 'textquery', 'fields': 'place_id', 'key': settings.MAP_API_KEY}
        response = requests.get(f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json', params=payload)
        response_dict = dict(response.json())
    except Exception:
        extra_fields_dict['places_result'] += 1
        print(f"{point['key']}:{point['name']}:{point['address']}")
        logger.log(logging.WARNING, f"{point['key']}:{point['name']}:{point['address']}")
    else:
        # place_idが取得できた場合
        if response_dict['candidates']:
            extra_fields_dict['places_id'] = response_dict['candidates'][0]['place_id']
        else:
            extra_fields_dict['places_result'] += 1
            print(f"{point['key']}:{point['name']}:{point['address']}")
            logger.log(logging.WARNING, f"{point['key']}:{point['name']}:{point['address']}")
    finally:
        now = datetime.now(timezone('Asia/Tokyo'))
        extra_fields_dict['places_date'] = now.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        extra_fields_dict['places_query'] = search_word
        return extra_fields_dict

# def send_notification(subject,
#                       body,
#                       from_email=settings.DEFAULT_FROM_EMAIL,
#                       to=None,
#                       bcc=None):
#     try:
#         EmailMessage(
#             subject=subject,
#             body=body,
#             from_email=from_email,
#             to=to,
#             bcc=bcc
#         ).send()
#     except Exception:
#         logger.log(logging.ERROR, traceback.format_exc())

def geocode(spot):
    try:
        url = 'https://map.yahooapis.jp/geocode/V1/geoCoder'
        payload = {'output': 'json', 'appid': settings.YAHOO['API_KEY'], 'query': spot['address']}
        response = session.request('GET', url, timeout=1, params=payload)

    except requests.exceptions.ConnectTimeout:
        # log
        print('タイムアウトしました')
    else:
        data = response.json()
        if 'Feature' in data:
            data = data['Feature'][0]
            coordinate = data['Geometry']['Coordinates'].split(',')
            lat = coordinate[1]
            lng = coordinate[0]
        else:
            lat = spot['geometry']['location']['lat']
            lng = spot['geometry']['location']['lng']
        spot_dict = {
            'name': spot['name'],
            'place_id': spot['place_id'],
            'address': spot['formatted_address'],
            'lat': lat,
            'lng': lng
        }
        return spot_dict

def read_words():
    print('U')
    get_geometry()

def get_geometry():
    spots = []
    with open(os.path.join(settings.BASE_DIR, 'client/assets/json/words.json'), mode='r',  encoding='utf-8') as f:
        dict_list = json.loads(f.read())
        for spots in dict_list:
            for spot in spots['spots']:
                spot = geocode(spot)

        # with open(f'./json/popular-spots.json', mode='w+', encoding='utf-8') as f:
        #     json.dump(spots, f, ensure_ascii=False, indent=2)
class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument('map_id')

    def handle(self, *args, **options):
        execute()
        # execute(options['map_id'])