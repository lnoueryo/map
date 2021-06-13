from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import JsonResponse, HttpResponse
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
import googlemaps
from datetime import datetime
import urllib.request
import json
import requests
from map.models import Station, Line, Company
from .serializers import StationSerializer, LineSerializer, CompanySerializer
from station_json.station import StationJson
import re
import csv
from rest_framework import status

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
        return HttpResponse(station, content_type='application/json; charset=UTF-8')
class LineAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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
    
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

class CSVCompanyAPI(APIView):

    def get(self, request):
        response = self.make_csv_file()
        header = self.make_column()
        delimiter = (request.GET.dict())['delimiter']
        response = self.write_csv(response, header, delimiter)
        """
        getの時にCSVをexportする関数。
        """
        return response

    def post(self, request):
        f = request.FILES['file'].read()
        f = f.decode(encoding='utf-8')
        f = f.split('\n')
        csv_list = []
        for row in f:
            row = str(row).split(',')
            if len(row) is 3:
                csv_list.append(row)
        print(csv_list[0][0])
        if csv_list[0][0] == 'name':
            del csv_list[0]
        companies = []
        for row in csv_list:
            company = Company(name=row[0],address=row[1],founded=row[2])
            companies.append(company)
        company = Company.objects.bulk_create(companies)
        serializer = CompanySerializer(company, many=True)
        return JsonResponse(serializer.data, safe=False)

    def make_csv_file(self):
        filename = "保存ルート一覧.csv"
        filename = filename.encode('utf-8', errors='ignore')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)
        return response

    def make_column(self):
        company_column = Company._meta.get_fields()
        company_column_value = []
        for index, row in enumerate(company_column):
            if index > 2 and index < 6:
                company_column_value.append(row.name)
        return company_column_value

    def write_csv(self, response, header, delimiter):
        if delimiter == 't':
            delimiter = '\t'
        writer = csv.writer(response, delimiter=delimiter)
        writer.writerow(header)
        for company in Company.objects.all():
            writer.writerow([company.name, company.address, company.founded])
        
        return response

    # def check_column():


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

