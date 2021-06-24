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
from .serializers import StationSerializer, LineSerializer, CompanySerializer, LineStationSerializer
from station_json.station import StationJson
import re
import csv
from rest_framework import status

class CompanyAPI(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True)
        return JsonResponse(serializer.data, safe=False)

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

class LineAPI(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        line = Line.objects.all()
        serializer = LineSerializer(line, many=True)
        data = self.parse(serializer.data)
        return JsonResponse(data, safe=False)

    def parse(self, data):
        for dict in data:
            dict['polygon'] = eval(dict['polygon'])
        return data

    def post(self, request):
        serializer = LineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class StationAPI(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        station = Station.objects.all()
        serializer = StationSerializer(station, many=True)
        return JsonResponse(serializer.data, safe=False)
    def post(self, request):
        serializer = StationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LineStationAPI(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        station = Line.objects.all()
        serializer = LineStationSerializer(station, many=True)
        return JsonResponse(serializer.data, safe=False)
    # def post(self, request):
    #     serializer = StationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LineDetailApi(APIView):
#     def put(self, request, pk, format=None):
#         print(pk)
#         return HttpResponse()
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CSVCompanyAPI(APIView):

    def get(self, request):
        response = make_csv_file()
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
        if csv_list[0][0] == 'name':
            del csv_list[0]
        companies = []
        for row in csv_list:
            company = Company(name=row[0],address=row[1],founded=row[2])
            companies.append(company)
        company = Company.objects.bulk_create(companies)
        serializer = CompanySerializer(company, many=True)
        return JsonResponse(serializer.data, safe=False)

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

class CSVLineAPI(APIView):

    def get(self, request):
        response = make_csv_file()
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
            row = str(row).split(request.data['delimiter'])
            if len(row) is 5:
                csv_list.append(row)
        if csv_list[0][0] == 'name':
            del csv_list[0]
        lines = []
        for row in csv_list:
            line = Line(name=row[0],polygon=row[1],color=row[2],line_code=row[3],company_id=Company.objects.get(id=row[4]))
            lines.append(line)
        line = Line.objects.bulk_create(lines)
        serializer = LineSerializer(line, many=True)
        return JsonResponse(serializer.data, safe=False)
        # return HttpResponse('hello')

    def make_column(self):
        line_column = Line._meta.get_fields()
        line_column_value = []
        for index, row in enumerate(line_column):
            if index > 1 and index < 7:
                line_column_value.append(row.name)
        return line_column_value

    def write_csv(self, response, header, delimiter):
        if delimiter == 't':
            delimiter = '\t'
        writer = csv.writer(response, delimiter=delimiter)
        writer.writerow(header)
        for line in Line.objects.all():
            polygon = self.make_json(line.polygon)
            writer.writerow([line.name, polygon, line.color, line.line_code, line.company_id.id])
        return response
    def make_json(self, polygon):
        import re
        polygon = re.sub('"', '', polygon)
        polygon = re.sub('lat', '"lat"', polygon)
        polygon = re.sub('lng', '"lng"', polygon)
        return polygon
class CSVStationAPI(APIView):

    def get(self, request):
        response = make_csv_file()
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
            if len(row) is 8:
                csv_list.append(row)
        if csv_list[0][0] == 'name' or csv_list[0][0] == 'id':
            del csv_list[0]
        stations = []
        for row in csv_list:
            station = Station(name=row[0],prefecture=row[1],lat=row[2],lng=row[3],company_id=Company.objects.get(id=row[4]),line_id=Line.objects.get(id=row[5]))
            stations.append(station)
        station = Station.objects.bulk_create(stations)
        serializer = StationSerializer(station, many=True)
        return JsonResponse(serializer.data, safe=False)


    def make_column(self):
        station_column = Station._meta.get_fields()
        station_column_value = []
        for index, row in enumerate(station_column):
            if index > 0 and index < 7:
                station_column_value.append(row.name)
        print(station_column_value)
        return station_column_value

    def write_csv(self, response, header, delimiter):
        if delimiter == 't':
            delimiter = '\t'
        writer = csv.writer(response, delimiter=delimiter)
        writer.writerow(header)
        for station in Station.objects.all():
            writer.writerow([station.name, station.prefecture, station.lat, station.lng, station.company_id.id, station.line_id.id])
        return response

def make_csv_file():
    filename = "保存ルート一覧.csv"
    filename = filename.encode('utf-8', errors='ignore')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)
    return response