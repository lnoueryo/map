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

class CompanyAPI(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        company = Company.objects.all()
        print(company)
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
