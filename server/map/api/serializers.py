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
    name = serializers.CharField()
    address = serializers.CharField()
    founded = serializers.CharField()
    class Meta: #　表示したり、create時のrequiredのキー
        model = Company
        fields = '__all__'

    # def validate(self, data):
    #     """Check that description and title are different"""
    #     print(data)
    #     # if data["name"] is not data["address"]:
    #     #     raise serializers.ValidationError("Title and Description must be different from one another")
    #     # return data
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