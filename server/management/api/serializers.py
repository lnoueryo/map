from users.models import NewUser
from map.models import Station, Line, Company
from rest_framework import exceptions, serializers
import json
from django.db import models

class StationSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    line = serializers.SerializerMethodField()
    class Meta: #　表示したり、create時のrequiredのキー
        model = Station
        fields = '__all__'

    def get_company(self, obj):
        return obj.company_id.name
    def get_line(self, obj):
        return obj.line_id.name
class LineSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    # stations = StationSerializer(many=True, read_only=True)
    class Meta: #　表示したり、create時のrequiredのキー
        model = Line
        fields = '__all__'
    def get_company(self, obj):
        return obj.company_id.name
class CompanySerializer(serializers.ModelSerializer):
    # lines = LineSerializer(many=True, read_only=True)
    # lines = serializers.StringRelatedField()
    # parent_id = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(),source='company.id')
    # station = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all(),source='station.company_id')
    name = serializers.CharField()
    address = serializers.CharField()
    founded = serializers.CharField()
    class Meta: #　表示したり、create時のrequiredのキー
        model = Company
        fields = '__all__'

    def validate_name(self, value):
        if len(value)>20:
            raise serializers.ValidationError("会社名は最大20文字までとなっております")
        return value
    def validate_address(self, value):
        if len(value)>60:
            raise serializers.ValidationError("住所は最大60文字までとなっております")
        return value
    def validate_founded(self, value):
        if len(value)>20:
            raise serializers.ValidationError("設立日は最大15文字までとなっております")
        return value

class LineStationSerializer(serializers.ModelSerializer):
    stations = StationSerializer(many=True, read_only=True)
    class Meta: #　表示したり、create時のrequiredのキー
        model = Line
        fields = '__all__'