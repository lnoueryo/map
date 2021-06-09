from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import JsonResponse, HttpResponse
from rest_framework.throttling import UserRateThrottle
import googlemaps
from datetime import datetime
import urllib.request
import json
import requests
from map.models import Station, Line, Company
from .serializers import StationSerializer, LineSerializer, CompanySerializer
from station_json.station import StationJson
import re

# import 
gmaps = googlemaps.Client(key='AIzaSyCLaTg7iFjqb20GWflIisy6P8VdOZUYmKA')
api_key = 'dj00aiZpPUhzbEhTY1dXWGZMaiZzPWNvbnN1bWVyc2VjcmV0Jng9ODk-'
class GeocodeAPI(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        reverse_geocode_result = gmaps.reverse_geocode((35.6703827, 139.6939093), language='ja')

        return JsonResponse(reverse_geocode_result, safe=False)

class ReverseGeocodeAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        endpoint = 'https://map.yahooapis.jp/geoapi/V1/reverseGeoCoder?output=json&appid=' + api_key + '&'
        dict = json.loads(request.body)
        lat = 'lat=' + str(dict['lat'])
        lng = 'lon=' + str(dict['lng'])
        query = lat + '&' + lng
        url = endpoint + query
        try:
            with requests.get(url) as response:
                data = response.json()
                data = data['Feature'][0]
                return JsonResponse(data, safe=False)
        except urllib.error.URLError as e:
            raise e.reason


class StationAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        station = Station.objects.all()
        serializer = StationSerializer(station, many=True)
        return JsonResponse(serializer.data, safe=False)

class StationDetailAPI(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        station = StationJson.get_line()
        print(JsonResponse(station, safe=False))
        # print(station)
        # request= request.GET
        # station = Station.objects.filter(line_name=request['line_name'])
        # station2 = station.filter(station_lat__range=(request['south'], request['north']))
        # station3 = station2.filter(station_lon__range=(request['west'], request['east']))
        # serializer = StationSerializer(station3, many=True)
        return HttpResponse(station, content_type='application/json; charset=UTF-8')
        # return JsonResponse(station, safe=False, json_dumps_params={'ensure_ascii': False})    
        # return JsonResponse(station, safe=False)    
        # f = open('../../station_json/yamanote.json', 'r', encoding='utf8')
        # data = f.read()
        # print(data)
        # f.close()
        # print(station2)
        # request= request.GET
        # station = Station.objects.filter(line_name=request['line_name'])
        # station2 = station.filter(station_lat__range=(request['south'], request['north']))
        # station3 = station2.filter(station_lon__range=(request['west'], request['east']))
        # serializer = StationSerializer(station3, many=True)
        # return JsonResponse(serializer.data, safe=False)    

# class PolygonAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         station = Station.objects.all()
#         serializer = StationSerializer(station, many=True)
#         return JsonResponse(serializer.data, safe=False)

class LineAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # for line in StationSerializer(Station.objects.all()):
        #     for a in line.values():
        #      print(a)
        # for line in Line.objects.prefetch_related('station'):
        #     print(line)
        line = Line.objects.all()
        serializer = LineSerializer(line, many=True)
        data = self.parse(serializer.data)
        return JsonResponse(data, safe=False)

    def parse(self, data):
        for dict in data:
            dict['polygon'] = eval(dict['polygon'])
        return data

class CompanyAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True)
        data = self.parse(serializer.data)
        return JsonResponse(data, safe=False)

    def parse(self, data):
        for company in data:
            for line in company['lines']:
                line['polygon'] = eval(line['polygon'])
        return data

class WikiAPI(APIView):

    def get(self, request):
        title = (request.GET.dict())['name'] + '駅'
        url = f'https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&titles={title}&rvprop=content&rvparse'
        try:
            with requests.get(url) as response:
                data = response.json()
                data = data['query']['pages']
                key = None
                for d in data:
                    key=d
                data = data[key]['revisions'][0]['*']
                data = self.parse(data)
                return HttpResponse(json.dumps(data, ensure_ascii=False))
        except urllib.error.URLError as e:
            error = {'status': 404}
            return HttpResponse(json.dumps(error, ensure_ascii=False))

    def post(self, request):
        title = request.data['name'] + '駅'
        url = f'https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&titles={title}&rvprop=content&rvparse'
        try:
            with requests.get(url) as response:
                data = response.json()
                data = data['query']['pages']
                key = None
                for d in data:
                    key=d
                data = data[key]['revisions'][0]['*']
                data = self.parse(data)
                return HttpResponse(json.dumps(data, ensure_ascii=False))
        except urllib.error.URLError as e:
            print(e.reason)
    def parse(self, data):
        pattern1 = r'(<table)(.+?)(box-出典の明記)(.+?)(</table>)'
        pattern2 = r'(<table)(.+?)(mbox-small)(.+?)(</table>)'
        data = re.sub(pattern1,'',data)
        data = re.sub('<a.*?>|</a>', '', data)
        return data

from django.shortcuts import render,redirect
from google.oauth2 import service_account
from google.cloud import storage
from django.conf import settings
service_account_info = {
#APIキーの中身
}
def download(request,filename):
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    client = storage.Client(
        credentials=credentials,
        project=credentials.project_id
    )
    bucket = client.get_bucket("g-map")
    blob = bucket.blob(filename)
    file = blob.download_as_bytes()
    response = HttpResponse(file,content_type='application/octet-stream')
    response["Content-Disposition"] = "filename="+filename
    return response
    # return HttpResponse('OK')
def practice(request):
    GS_CREDENTIALS = getattr(settings, "GS_CREDENTIALS", None)
    # credentials = service_account.Credentials.from_service_account_info(service_account_info)
    client = storage.Client(
        credentials=GS_CREDENTIALS,
        project=GS_CREDENTIALS.project_id
    )
    bucket = client.get_bucket("g-map")
    blob = bucket.blob('qiita1.png')
    # print(bucket)
    # file = blob.download_as_bytes()
    # response = HttpResponse(file,content_type='application/octet-stream')
    # response["Content-Disposition"] = "filename="+'qiita11.png'
    # return response
    return HttpResponse(blob.exists())

