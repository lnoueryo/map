from django.http import HttpResponse, JsonResponse
import requests
import json
import re
import time
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from bs4 import BeautifulSoup
from bs4.element import Comment
from rest_framework.views import APIView
from django.conf import settings

API_KEY = settings.YAHOO['API_KEY']

class ReverseGeocodeAPI(APIView):
    """
    リバースジオコーダAPI
    lat, lon
    https://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/reversegeocoder.html
    """
    def get(self, request):
        params = request.GET.dict()
        payload = {'appid': API_KEY, 'output': 'json', 'lat': params['lat'], 'lon': params['lng']}
        url = 'https://map.yahooapis.jp/geoapi/V1/reverseGeoCoder'
        try:
            response = requests.get(url, params=payload)
        except Exception as e:
            return JsonResponse(error_response(502), status=502, safe=False)
        else:
            data = response.json()
            data = data['Feature'][0]
            return JsonResponse(data, safe=False)

class LocalSearchAPI(APIView):
    """
    ローカルサーチAPI
    query(地域・拠点情報・業種), gc, ac, bbox
    https://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/localsearch.html
    """
    def get(self, request):
        params = request.GET.dict()
        bbox = None
        if 'bounds' in params:
            bounds = json.loads(params['bounds'])
            bbox = f'{bounds["west"]},{bounds["south"]},{bounds["east"]},{bounds["north"]}'
        payload = {
            'appid': API_KEY,
            'output': 'json',
            'query': params['searchWord'] if 'searchWord' in params else None,
            'gc': params['gc'] if 'gc' in params else None,
            'ac': params['city_code'] if 'city_code' in params else None,
            'results': 100,
            'bbox': bbox
        }
        url = 'https://map.yahooapis.jp/search/local/V1/localSearch'
        try:
            response = requests.get(url, params=payload)
        except Exception as e:
            return JsonResponse(error_response(502), status=502, safe=False)
        else:
            data = response.json()
            data = data['Feature'][0]
            return JsonResponse(data, safe=False)

class PlaceInfoAPI(APIView):
    """
    場所情報API
    lat, lon
    https://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/placeinfo.html
    """

    def get(self, request):
        params = request.GET.dict()
        payload = {
            'appid': API_KEY,
            'output': 'json',
            'lat': params['lat'],
            'lon': params['lng']
        }
        url = 'https://map.yahooapis.jp/placeinfo/V1/get'
        try:
            response = requests.get(url, params=payload)
        except Exception as e:
            return JsonResponse(error_response(502), status=502, safe=False)
        else:
            data = response.json()
            data = data['ResultSet']['Result']
            return JsonResponse(data, safe=False)

    def create_coordinates(response_dict):
        coordinates_list = response_dict['Geometry']['Coordinates'].split(',')
        response_dict['lat'] = coordinates_list[1]
        response_dict['lng'] = coordinates_list[0]
        del response_dict['Gid']
        del response_dict['Geometry']
        del response_dict['Country']
        return response_dict

class ContentGeocoderAPI(APIView):
    """
    コンテンツジオコーダAPI
    query, category
    https://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/contentsgeocoder.html
    """

    def get(self, request):
        params = request.GET.dict()
        payload = {'appid': API_KEY, 'output': 'json', 'query': params['searchWord'], 'category': 'landmark', 'results': 10}
        url = 'https://map.yahooapis.jp/geocode/cont/V1/contentsGeoCoder'
        try:
            response = requests.get(url, params=payload)
        except Exception as e:
            return JsonResponse(error_response(502), status=502, safe=False)
        else:
            data = response.json()
            data = data['Feature'][0]
            return JsonResponse(data, safe=False)

def error_response(status_code):
    if status_code == 502:
        return {'message': '現在アクセスが集中しているため、時間をおいて再度お試しください。'}