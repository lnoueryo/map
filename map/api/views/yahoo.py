from django.http import HttpResponse, JsonResponse
import requests
import json
import re
import time
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import urllib.request

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
            with requests.get(url, params=payload) as response:
                data = response.json()
                data = data['Feature'][0]
                return JsonResponse(data, safe=False)
        except urllib.error.URLError as e:
            raise e.reason

class LocalSearchAPI(APIView):
    """
    ローカルサーチAPI
    query(地域・拠点情報・業種), gc, ac, bbox
    https://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/localsearch.html
    """
    def get(self, request):
        params = request.GET.dict()
        payload = {'appid': API_KEY, 'output': 'json', 'query': params['searchWord'], 'gc': params['gc'], 'ac': params['city_code'], 'results': 100, 'bbox': params['bounds']}
        url = 'https://map.yahooapis.jp/search/local/V1/localSearch'
        try:
            with requests.get(url, params=payload) as response:
                data = response.json()
                data = data['Feature'][0]
                return JsonResponse(data, safe=False)
        except urllib.error.URLError as e:
            raise e.reason

class PlaceInfoAPI(APIView):
    """
    場所情報API
    lat, lon
    https://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/placeinfo.html
    """

    def get(self, request):
        params = request.GET.dict()
        payload = {'appid': API_KEY, 'output': 'json', 'query': params['searchWord'], 'gc': params['gc'], 'ac': params['city_code'], 'results': 100, 'bbox': params['bounds']}
        url = 'https://map.yahooapis.jp/search/local/V1/localSearch'
        try:
            with requests.get(url, params=payload) as response:
                data = response.json()
                data = data['Feature'][0]
                return JsonResponse(data, safe=False)
        except urllib.error.URLError as e:
            raise e.reason

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
            with requests.get(url, params=payload) as response:
                data = response.json()
                data = data['Feature'][0]
                return JsonResponse(data, safe=False)
        except urllib.error.URLError as e:
            raise e.reason