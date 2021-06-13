from users.models import NewUser
from map.models import Station, Line, Company
from rest_framework import exceptions, serializers
import json

class StationSerializer(serializers.ModelSerializer):

    class Meta: #　表示したり、create時のrequiredのキー
        model = Station
        fields = '__all__'

class LineSerializer(serializers.ModelSerializer):
    class Meta: #　表示したり、create時のrequiredのキー
        model = Line
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    lines = LineSerializer(many=True, read_only=True)
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