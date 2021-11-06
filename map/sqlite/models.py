import json
import ast
import datetime

import sqlalchemy as sa
from sqlalchemy.orm import backref, sessionmaker, relationship
from sqlalchemy import (Table, Column, Integer, String, ForeignKey, DateTime, text, Float, and_)
from sqlalchemy.dialects.mysql.base import BIGINT, LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import current_timestamp
from datetime import timedelta
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Text
from sqlalchemy.dialects import sqlite
from sqlalchemy.dialects import mysql
from pathlib import Path

TextType = Text()
TextType = TextType.with_variant(mysql.LONGTEXT(), 'mysql')
TextType = TextType.with_variant(sqlite.TEXT(), 'sqlite')

Base = declarative_base()

class LineStation(Base):
    """
    LineStationテーブルクラス
    """

    # テーブル名
    __tablename__ = 'lines_stations'

    # 個々のカラムを定義
    id = Column(BIGINT, primary_key=True)
    line_id = Column(BIGINT, ForeignKey('lines.id'), primary_key=True)
    station_id = Column(BIGINT, ForeignKey('stations.id'), primary_key=True)
    line = relationship('Line', backref='lines_junctions')
    station = relationship('Station', backref='stations_junctions')

class Company(Base):
    """
    Companyテーブルクラス
    """

    # テーブル名
    __tablename__ = 'companies'

    # 個々のカラムを定義
    id = Column(BIGINT, primary_key=True)
    name = Column(String(20))
    address = Column(String(20))
    founded = Column(String(20))
    # created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    # updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    lines = relationship("Line", backref="companies")

    def to_dict(self):
        company_dict = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'lines': [line.to_dict() for line in self.lines]
        }
        return company_dict

    def join_dict(self):
        company_dict = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
        }
        return company_dict

class Line(Base):
    """
    Lineテーブルクラス
    """

    # テーブル名
    __tablename__ = 'lines'

    id = Column(BIGINT, primary_key=True)
    company_id = Column(BIGINT, ForeignKey('companies.id'))
    prefecture_id = Column(String(3), ForeignKey('prefectures.id'), nullable=True)
    name = Column(String(20))
    polygon = Column(TextType)
    color = Column(String(20))
    company = relationship('Company')
    # created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    # updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    stations = relationship(
        'Station',
        secondary=LineStation.__tablename__,
    )

    def to_dict(self):
        polygon = eval(self.polygon)
        line_dict = {
            'id': self.id,
            'company_id': self.company_id,
            'name': self.name,
            'polygon': polygon,
            'color': self.color,
            'stations': [station.join_dict() for station in self.stations]
        }
        return line_dict

    def join_dict(self):
        polygon = eval(self.polygon)
        line_dict = {
            'id': self.id,
            'company_id': self.company_id,
            'name': self.name,
            'polygon': polygon,
            'color': self.color,
        }
        return line_dict

class Station(Base):
    """
    Stationテーブルクラス
    """

    # テーブル名
    __tablename__ = 'stations'

    # 個々のカラムを定義
    id = Column(BIGINT, primary_key=True)
    company_id = Column(BIGINT, ForeignKey('companies.id'))
    name = Column(String(20))
    address = Column(String(20))
    prefecture_id = Column(String(3), ForeignKey('prefectures.id'))
    city_code = Column(String(6), ForeignKey('cities.id'))
    place_id = Column(String(50))
    place_ids = Column(TextType, nullable=True)
    place_result = Column(String(255))
    geohash = Column(String(10))
    search_text = Column(String(255))
    lat = Column(Float)
    lng = Column(Float)
    # created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    # updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    lines = relationship(
        'Line',
        secondary='lines_stations',
    )
    company = relationship('Company')

    def to_dict(self):
        station_dict = {
            'id': self.id,
            'company_id': self.company_id,
            'name': self.name,
            'address': self.address,
            'prefecture_id': self.prefecture_id,
            'city_code': self.city_code,
            'place_id': self.place_id,
            'place_ids': self.place_ids,
            'place_result': self.place_result,
            'geohash': self.geohash,
            'lat': self.lat,
            'lng': self.lng,
            'search_text': self.search_text,
            'lines': [line.to_dict() for line in self.lines],
            'company': self.company.join_dict()
        }
        return station_dict

    def join_dict(self):
        station_dict = {
            'id': self.id,
            'company_id': self.company_id,
            'name': self.name,
            'address': self.address,
            'prefecture_id': self.prefecture_id,
            'city_code': self.city_code,
            'place_id': self.place_id,
            'place_ids': self.place_ids,
            'place_result': self.place_result,
            'geohash': self.geohash,
            'lat': self.lat,
            'lng': self.lng,
            'search_text': self.search_text,
        }
        return station_dict


class Prefecture(Base):
    """
    Prefectureテーブルクラス
    """

    # テーブル名
    __tablename__ = 'prefectures'

    # 個々のカラムを定義
    id = Column(String(3), nullable=False, index=True, primary_key=True)
    name = Column(String(20))
    lat = Column(Float)
    lng = Column(Float)
    # created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    # updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    cities = relationship(
        'City',
        backref='prefectures',
    )
    stations = relationship(
        'Station',
        backref='prefectures',
    )
    spots = relationship('Spot', backref='prefectures')

    def to_dict(self):
        prefecture_dict = {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lng': self.lng,
        }
        return prefecture_dict

    def with_city_dict(self):
        prefecture_dict = {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lng': self.lng,
            'cities': self.city_dict_list(self.cities, spots=True)
        }
        return prefecture_dict

    def city_dict_list(self, cities, spots):
        city_dict_list = []
        if spots:
            for city in cities:
                city_dict = {
                    'id': city.id,
                    'prefecture_id': city.prefecture_id,
                    'name': city.name,
                    'lat': city.lat,
                    'lng': city.lng,
                    'polygons': eval(city.polygons),
                    'layouts': city.layouts,
                    'spots': self.spot_dict_list(city.spots)
                }
                city_dict_list.append(city_dict)
        else:
            for city in cities:
                city_dict = {
                    'id': city.id,
                    'prefecture_id': city.prefecture_id,
                    'name': city.name,
                    'lat': city.lat,
                    'lng': city.lng,
                    'polygons': eval(city.polygons),
                    'layouts': city.layouts,
                    'created_at': city.created_at,
                    'updated_at': city.updated_at,
                }
                city_dict_list.append(city_dict)
        return city_dict_list

    def spot_dict_list(self, spots):
        spot_dict_list = []
        for spot in spots:
            spot_dict = {
                'id': spot.id,
                'prefecture_id': spot.prefecture_id,
                'city_code': spot.city_code,
                'name': spot.name,
                'lat': spot.lat,
                'lng': spot.lng,
                'place_id': spot.place_id,
                'address': spot.address,
                'geohash': spot.geohash,
            }
            spot_dict_list.append(spot_dict)
        return spot_dict_list

    def with_station_dict(self):
        prefecture_dict = {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lng': self.lng,
            'stations': self.station_dict(self.stations)
        }
        return prefecture_dict

    def station_dict(self, stations):
        station_dict_list = []
        for station in stations:
            station_dict = {
                'id': station.id,
                'company_id': station.company_id,
                'name': station.name,
                'address': station.address,
                'prefecture_id': station.prefecture_id,
                'city_code': station.city_code,
                'place_id': station.place_id,
                'place_ids': station.place_ids,
                'place_result': station.place_result,
                'geohash': station.geohash,
                'lat': station.lat,
                'lng': station.lng,
                'search_text': station.search_text,
                'lines': [line.join_dict() for line in station.lines],
                'company': station.company.join_dict()
            }
            station_dict_list.append(station_dict)
        return station_dict_list
class City(Base):
    """
    Cityテーブルクラス
    """

    # テーブル名
    __tablename__ = 'cities'

    # 個々のカラムを定義
    
    id = Column(String(6), nullable=False, index=True, primary_key=True)
    prefecture_id = Column(String(3), ForeignKey('prefectures.id'))
    name = Column(String(20))
    lat = Column(Float)
    lng = Column(Float)
    polygons = Column(TextType)
    layouts = Column(TextType)
    columns = Column(TextType)
    # created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    # updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    stations = relationship(
        'Station',
        backref='cities',
    )
    prefecture = relationship('Prefecture')
    facility = relationship(
        'Facility',
        back_populates="city",
        uselist=False
    )
    occupation = relationship(
        'Occupation',
        back_populates="city",
        uselist=False
    )
    population = relationship(
        'Population',
        back_populates="city",
        uselist=False
    )
    spots = relationship('Spot', backref='cities')
    towns = relationship('Town', backref='towns')

    def to_dict(self):
        city_dict = {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lng': self.lng,
        }
        return city_dict

    def to_city_dict(self):
        spots = [spot.join_dict() for spot in self.spots] if self.spots else []
        towns = [town.to_dict() for town in self.towns] if self.towns else []
        stations = [station.to_dict() for station in self.stations] if self.stations else []
        layouts = eval(self.layouts) if self.layouts else ''
        columns = eval(self.columns) if self.columns else ''
        city_dict = {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lng': self.lng,
            'polygons': eval(self.polygons),
            'layouts': layouts,
            'columns': columns,
            'facility': self.facility.to_dict(),
            'occupation': self.occupation.to_dict(),
            'population': self.population.to_dict(),
            'spots': spots,
            'towns': towns,
            'stations': stations
        }
        return city_dict

    def join_dict(self):
        city_dict = {
            'id': self.id,
            'name': self.name,
            'lat': self.place_result,
            'lng': self.geohash,
        }
        return city_dict

class Facility(Base):
    """
    Facilityテーブルクラス
    """

    # テーブル名
    __tablename__ = 'facilities'

    # 個々のカラムを定義
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_code = Column(String(6), ForeignKey('cities.id'))
    name = Column(String(10))
    community_center = Column(Integer)
    library = Column(Integer)
    house = Column(Integer)
    shop = Column(Integer)
    restaurant = Column(Integer)
    store = Column(Integer)
    supermarket = Column(Integer)
    hospital = Column(Integer)
    clinic = Column(Integer)
    dental_clinic = Column(Integer)
    nursing_facility = Column(Integer)
    orphanage = Column(Integer)
    nursery_center = Column(Integer)
    kindergarten = Column(Integer)
    elementary_school = Column(Integer)
    junior_high_school = Column(Integer)
    high_school = Column(Integer)
    occupation_area = Column(Float)
    # created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    # updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    city = relationship('City')


    def to_dict(self):
        facility_dict = {
            'id': self.id,
            'city_code': self.city_code,
            'name': self.name,
            'community_center': self.community_center,
            'library': self.library,
            'house': self.house,
            'shop': self.shop,
            'restaurant': self.restaurant,
            'store': self.store,
            'supermarket': self.supermarket,
            'hospital': self.hospital,
            'clinic': self.clinic,
            'dental_clinic': self.dental_clinic,
            'nursing_facility': self.nursing_facility,
            'orphanage': self.orphanage,
            'nursery_center': self.nursery_center,
            'kindergarten': self.kindergarten,
            'elementary_school': self.elementary_school,
            'junior_high_school': self.junior_high_school,
            'high_school': self.high_school,
            'occupation_area': self.occupation_area,
        }
        return facility_dict

class Occupation(Base):
    """
    Occupationテーブルクラス
    """

    # テーブル名
    __tablename__ = 'occupations'

    # 個々のカラムを定義
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_code = Column(String(6), ForeignKey('cities.id'))
    name = Column(String(10))
    taxpayers = Column(Integer)
    kindergartener = Column(Integer)
    elementary_school_teacher = Column(Integer)
    elementary_school_student = Column(Integer)
    junior_high_school_student = Column(Integer)
    high_school_student = Column(Integer)
    working_age_population = Column(Integer)
    employed_population = Column(Integer)
    unemployed_population = Column(Integer)
    executive_officer = Column(Integer)
    owners = Column(Integer)
    self_employed = Column(Integer)
    family_employees = Column(Integer)
    workers_in_your_city = Column(Integer)
    workers_in_another_city = Column(Integer)
    employees_working_in_office = Column(Integer)
    commuting_population_from_other_city = Column(Integer)
    doctor = Column(Integer)
    dentist = Column(Integer)
    pharmacist = Column(Integer)
    # created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    # updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    city = relationship('City')

    def to_dict(self):
        occupation_dict = {
            'id': self.id,
            'city_code': self.city_code,
            'name': self.name,
            'taxpayers': self.taxpayers,
            'kindergartener': self.kindergartener,
            'elementary_school_teacher': self.elementary_school_teacher,
            'elementary_school_student': self.elementary_school_student,
            'junior_high_school_student': self.junior_high_school_student,
            'high_school_student': self.high_school_student,
            'working_age_population': self.working_age_population,
            'employed_population': self.employed_population,
            'unemployed_population': self.unemployed_population,
            'executive_officer': self.executive_officer,
            'self_employed': self.self_employed,
            'family_employees': self.family_employees,
            'workers_in_your_city': self.workers_in_your_city,
            'workers_in_another_city': self.workers_in_another_city,
            'employees_working_in_office': self.employees_working_in_office,
            'commuting_population_from_other_city': self.commuting_population_from_other_city,
            'doctor': self.doctor,
            'dentist': self.dentist,
            'pharmacist': self.pharmacist,
        }
        return occupation_dict

class Population(Base):
    """
    Populationテーブルクラス
    """

    # テーブル名
    __tablename__ = 'populations'

    # 個々のカラムを定義
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_code = Column(String(6), ForeignKey('cities.id'))
    name = Column(String(10))
    population = Column(Integer)
    japanese = Column(Integer)
    foreign = Column(Integer)
    basic_resident_register_population = Column(Integer)
    under15 = Column(Integer)
    between15_64 = Column(Integer)
    over65 = Column(Integer)
    daytime = Column(Integer)
    births = Column(Integer)
    death = Column(Integer)
    total_households = Column(Integer)
    households = Column(Integer)
    nuclear_family_households = Column(Integer)
    single_households = Column(Integer)
    transferees = Column(Integer)
    mover = Column(Integer)
    marriages = Column(Integer)
    divorces = Column(Integer)
    area = Column(Float)
    resident_area = Column(Float)
    # created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    # updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    city = relationship('City')

    def to_dict(self):
        population_dict = {
            'id': self.id,
            'city_code': self.city_code,
            'name': self.name,
            'population': self.population,
            'japanese': self.japanese,
            'foreign': self.foreign,
            'basic_resident_register_population': self.basic_resident_register_population,
            'under15': self.under15,
            'between15_64': self.between15_64,
            'over65': self.over65,
            'daytime': self.daytime,
            'births': self.births,
            'death': self.death,
            'total_households': self.total_households,
            'households': self.households,
            'nuclear_family_households': self.nuclear_family_households,
            'single_households': self.single_households,
            'transferees': self.transferees,
            'mover': self.mover,
            'marriages': self.marriages,
            'divorces': self.divorces,
            'area': self.area,
            'resident_area': self.resident_area,
        }
        return population_dict

class Spot(Base):
    """
    Populationテーブルクラス
    """

    # テーブル名
    __tablename__ = 'spots'

    # 個々のカラムを定義
    id = Column(BIGINT, primary_key=True)
    prefecture_id = Column(String(3), ForeignKey('prefectures.id'))
    city_code = Column(String(6), ForeignKey('cities.id'))
    name = Column(String(100))
    place_id = Column(String(100))
    address = Column(String(100))
    geohash = Column(String(10))
    lat = Column(Float)
    lng = Column(Float)
    # created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    # updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    city = relationship('City')

    def to_dict(self):
        population_dict = {
            'id': self.id,
            'city_code': self.city_code,
            'name': self.name,
            'population': self.population,
            'japanese': self.japanese,
            'foreign': self.foreign,
            'basic_resident_register_population': self.basic_resident_register_population,
            'under15': self.under15,
            'between15_64': self.between15_64,
            'over65': self.over65,
            'daytime': self.daytime,
            'births': self.births,
            'death': self.death,
            'total_households': self.total_households,
            'households': self.households,
            'nuclear_family_households': self.nuclear_family_households,
            'single_households': self.single_households,
            'transferees': self.transferees,
            'mover': self.mover,
            'marriages': self.marriages,
            'divorces': self.divorces,
            'area': self.area,
            'resident_area': self.resident_area,
        }
        return population_dict

class Spot(Base):
    """
    Populationテーブルクラス
    """

    # テーブル名
    __tablename__ = 'spots'
    __table_args__ = {'extend_existing': True}

    # 個々のカラムを定義
    id = Column(BIGINT, primary_key=True)
    prefecture_id = Column(String(3), ForeignKey('prefectures.id'))
    city_code = Column(String(6), ForeignKey('cities.id'))
    name = Column(String(100))
    place_id = Column(String(100))
    address = Column(String(100))
    geohash = Column(String(10))
    lat = Column(Float)
    lng = Column(Float)
    # created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    # updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    city = relationship('City')

    def to_dict(self):
        prefecture_dict = {
            'id': self.id,
            'prefecture_id': self.prefecture_id,
            'city_code': self.city_code,
            'name': self.name,
            'place_id': self.place_id,
            'address': self.address,
            'geohash': self.geohash,
            'lat': self.lat,
            'lng': self.lng,
            'lines': [city.to_dict() for city in self.cities]
        }
        return prefecture_dict

    def join_dict(self):
        spot_dict = {
            'id': self.id,
            'prefecture_id': self.prefecture_id,
            'city_code': self.city_code,
            'name': self.name,
            'place_id': self.place_id,
            'address': self.address,
            'geohash': self.geohash,
            'lat': self.lat,
            'lng': self.lng,
        }
        return spot_dict

class Town(Base):
    """
    Townテーブルクラス
    """

    # テーブル名
    __tablename__ = 'towns'

    # 個々のカラムを定義
    id = Column(Integer, primary_key=True, autoincrement=True)
    prefecture_id = Column(String(3), ForeignKey('prefectures.id'))
    city_code = Column(String(6), ForeignKey('cities.id'))
    name = Column(String(20))
    address = Column(String(100))
    count = Column(Integer)
    count_ratio = Column(Float)
    geohash = Column(String(10))
    lat = Column(Float)
    lng = Column(Float)
    layouts = Column(TextType)
    columns = Column(TextType)
    city = relationship('City')
    # created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    # updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def to_dict(self):
        layouts = eval(self.layouts) if self.layouts else ''
        columns = eval(self.columns) if self.columns else ''
        town_dict = {
            'id': self.id,
            'prefecture_id': self.prefecture_id,
            'city_code': self.city_code,
            'name': self.name,
            'address': self.address,
            'count': self.count,
            'count_ratio': self.count_ratio,
            'lat': self.lat,
            'lng': self.lng,
            'geohash': self.geohash,
            'layouts': layouts,
            'columns': columns,
        }
        return town_dict

    def join_dict(self):
        town_dict = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'lat': self.lat,
            'lng': self.lng,
        }
        return town_dict

def change_time(time):
    added_timezone = time + timedelta(hours=9)
    return added_timezone.strftime('%Y/%m/%d %H:%M:%S')
