from django.db import models
from django.contrib.postgres.fields import JSONField
class Price(models.Model):
    municipality_code = models.SmallIntegerField(blank=True, null=True)
    prefecture = models.CharField(max_length=10)
    municipality = models.CharField(max_length=50)
    district_name = models.CharField(max_length=10)
    trade_price = models.BigIntegerField(blank=True, null=True)
    floor_plan = models.CharField(max_length=10)
    area = models.CharField(max_length=50)
    building_year = models.CharField(max_length=10)
    period = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'price'
    def __str__(self):
        return self.district_name

class Company(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.TextField()
    address = models.TextField()
    founded = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = False
        db_table = 'company'

    def __str__(self):
        return f'{self.name}'

class Line(models.Model):
    name = models.CharField(max_length=50)
    polygon = models.TextField()
    color = models.CharField(max_length=50, blank=True, null=True)
    line_code = models.IntegerField(unique=True)
    company_id = models.ForeignKey(Company, db_column='company_id', to_field='id', related_name='lines', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'line'


    def __str__(self):
        return f'{self.name}'

class Station(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    prefecture = models.CharField(max_length=50)
    lat = models.FloatField()
    lng = models.FloatField()
    company_id = models.ForeignKey(Company, db_column='company_id', to_field='id', related_name='stations', on_delete=models.PROTECT)
    line_id = models.ForeignKey(Line, db_column='line_id', to_field='id', related_name='stations', on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'station'

    def __str__(self):
        return f'{self.name}'

# class Station(models.Model):
#     pref_code = models.SmallIntegerField()
#     pref_name = models.CharField(max_length=50)
#     station_code = models.IntegerField()
#     station_name = models.CharField(max_length=50)
#     station_yomi = models.CharField(max_length=50)
#     station_lat = models.FloatField()
#     station_lon = models.FloatField()
#     line_code = models.ForeignKey(Line, db_column='line_code', to_field='line_code', related_name='stations', on_delete=models.CASCADE)
#     line_name = models.CharField(max_length=50)
#     order = models.IntegerField()
#     company_code = models.CharField(max_length=10)
#     company_name = models.CharField(max_length=10)

#     class Meta:
#         managed = False
#         db_table = 'station'

#     def __str__(self):
#         return f'{self.station_name} : {self.line_name} : {self.company_name}'

