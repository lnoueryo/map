from users.models import NewUser
from map.models import Station, Line, Company
from rest_framework import exceptions, serializers
import json

class StationSerializer(serializers.ModelSerializer):
    
    class Meta: #　表示したり、create時のrequiredのキー
        model = Station
        fields = '__all__'
        # exclude = ['pref_code', 'station_code', 'station_yomi', 'line_code', 'company_code']

class LineSerializer(serializers.ModelSerializer):
    stations = StationSerializer(many=True, read_only=True)
    class Meta: #　表示したり、create時のrequiredのキー
        model = Line
        # fields = ['id']
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    lines = LineSerializer(many=True, read_only=True)
    class Meta: #　表示したり、create時のrequiredのキー
        model = Company
        fields = '__all__'

