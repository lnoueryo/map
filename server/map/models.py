#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Mapに使用するModel

Prefecture
City
Population
Occupation
Facility
Town
Spot
Company
Line
LineStation
Station

"""
from datetime import timedelta

from sqlalchemy.orm import relationship
from sqlalchemy import (Table, Column, Integer, String, ForeignKey, DateTime, text, Float, and_)
from sqlalchemy.dialects.mysql.base import BIGINT, LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import current_timestamp
from django.conf import settings

engine = settings.ENGINE
Base = declarative_base()

class LineStation(Base):
    """LineStationテーブルクラス

    linesテーブルとstationsテーブルを繋げる
    中間テーブル

    Attributes:
        id (int): プライマリーキー
        line_id (int): linesテーブルとつなぐ外部キー
        station_id (int): stationsテーブルとつなぐ外部キー
        line (:obj:Line): linesテーブル(ManyToMany)
        station (:obj:Station): stationsテーブル(ManyToMany)
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
    """Companyテーブルクラス

    companiesテーブルのカラムの定義
    オブジェクトを辞書変換する関数の定義

    Attributes:
        id (int): プライマリーキー
        name (str): 鉄道会社名
        address (str): 本社の住所
        founded (str): 設立日
        created_at (timestamp): レコード作成時間
        updated_at (timestamp): レコード更新時間
        lines (:obj:Line): linesテーブル(OneToMany)
    """

    # テーブル名
    __tablename__ = 'companies'

    # 個々のカラムを定義
    id = Column(BIGINT, primary_key=True)
    name = Column(String(20))
    address = Column(String(20))
    founded = Column(String(20))
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    lines = relationship("Line", backref="companies")

    def to_join_line_station_dict(self):
        """linesとstationsが結合されたテーブルの辞書変換関数

        linesテーブルとstationsテーブルが結合された
        Companyオブジェクトを辞書型に変換する関数

        Returns:
            辞書型: 下記の辞書が返される
        """
        company_dict = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'founded': self.founded,
            'lines': self.to_line_station_dict(self.lines)
        }
        return company_dict

    def to_line_station_dict(self, lines):
        """stationsが結合されたテーブルの辞書変換関数

        stationsテーブルが結合された
        Lineオブジェクトを辞書型に変換する関数

        Args:
            lines (:obj:Line[]): Lineオブジェクトのリスト

        Returns:
            辞書型: 下記の辞書が返される

        """
        line_dict_list = []
        for line in lines:
            line_dict = {
                'id': line.id,
                'name': line.name,
                'polygon': line.polygon,
                'color': line.color,
                'stations': self.to_station_dict(line.stations)
            }
            line_dict_list.append(line_dict)
        return line_dict_list

    def to_station_dict(self, stations):
        """stationsテーブルの辞書変換関数

        Stationオブジェクトを辞書型に変換する関数

        Args:
            stations (:obj:Station[]): Stationオブジェクトのリスト

        Returns:
            辞書型: 下記の辞書が返される

        """
        station_dict_list = []
        for station in stations:
            station_dict = {
                'id': station.id,
                'name': station.name,
                'lat': station.lat,
                'lng': station.lng,
            }
            station_dict_list.append(station_dict)
        return station_dict_list

    def to_company_dict(self):
        """結合のないcompaniesテーブルの辞書変換関数

        Companyオブジェクトを辞書型に変換する関数

        Returns:
            辞書型: 下記の辞書が返される

        """
        company_dict = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'founded': self.founded,
        }
        return company_dict

class Line(Base):
    """Lineテーブルクラス

    linesテーブルのカラムの定義
    オブジェクトを辞書変換する関数の定義

    Attributes:
        id (int): プライマリーキー
        company_id (int): companiesテーブルとつなぐ外部キー
        prefecture_id (str): prefecturesテーブルとつなぐ外部キー
        name (str): 路線名
        polygon (str): {lat: float, lng: float}の文字列化されたJSON
        color (str): 路線のカラーコード
        created_at (timestamp): レコード作成時間
        updated_at (timestamp): レコード更新時間
        company (:obj:Compamy): companiesテーブル(ManyToOne)
        stations (:obj:Station): stationsテーブル(ManyToMany)
    """

    # テーブル名
    __tablename__ = 'lines'

    id = Column(BIGINT, primary_key=True)
    company_id = Column(BIGINT, ForeignKey('companies.id'))
    prefecture_id = Column(String(3), ForeignKey('prefectures.id'), nullable=True)
    name = Column(String(20))
    polygon = Column(LONGTEXT)
    color = Column(String(20))
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    company = relationship('Company')
    stations = relationship(
        'Station',
        secondary=LineStation.__tablename__,
    )

    def to_line_dict(self):
        """結合のないlinesテーブルの辞書変換関数

        Lineオブジェクトを辞書型に変換する関数

        Returns:
            辞書型: 下記の辞書が返される

        """
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
    """Stationテーブルクラス

    stationsテーブルのカラムの定義
    オブジェクトを辞書変換する関数の定義

    Attributes:
        id (int): プライマリーキー
        company_id (int): companiesテーブルとつなぐ外部キー
        prefecture_id (str): prefecturesテーブルとつなぐ外部キー
        name (str): 駅名
        address (str): 駅の住所
        city_code (str): citiesテーブルとつなぐ外部キー
        place_id (str): Google Maps APIのplace_id
        place_ids (str): 複数取れた場合のplace_idの文字列JSON
        place_result (str): 取得失敗回数と更新の日時が格納された文字列JSON
        geohash (str): 駅のgeohash
        lat (float): 駅の緯度
        lng (float): 駅の経度
        search_text (str): 駅の検索に必要な文字
        created_at (timestamp): レコード作成時間
        updated_at (timestamp): レコード更新時間
        company (:obj:Compamy): companiesテーブル(ManyToOne)
        lines (:obj:Line[]): linesテーブル(ManyToMany)
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
    place_ids = Column(LONGTEXT, nullable=True)
    place_result = Column(String(255))
    geohash = Column(String(10))
    lat = Column(Float)
    lng = Column(Float)
    search_text = Column(String(255))
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    lines = relationship(
        'Line',
        secondary='lines_stations',
    )
    company = relationship('Company')

    def to_join_company_line_station_dict(self):
        """companies, lines, stationsが結合されたテーブルの辞書変換関数

        companiesテーブル、linesテーブルとstationsテーブルが結合された
        Stationオブジェクトを辞書型に変換する関数

        Returns:
            辞書型: 下記の辞書が返される
        """
        station_dict = {
            'id': self.id,
            'company_id': self.company_id,
            'name': self.name,
            'address': self.address,
            'prefecture_id': self.prefecture_id,
            'city_code': self.city_code,
            'place_id': self.place_id,
            'geohash': self.geohash,
            'lat': self.lat,
            'lng': self.lng,
            'search_text': self.search_text,
            'lines': self.to_line_station_dict(self.lines),
            'company': self.company.to_company_dict()
        }
        return station_dict

    def to_line_station_dict(self, lines):
        """stationsが結合されたテーブルの辞書変換関数

        stationsテーブルが結合された
        Lineオブジェクトを辞書型に変換する関数

        Args:
            lines (:obj:Line[]): Lineオブジェクトのリスト

        Returns:
            辞書型: 下記の辞書が返される

        """
        line_dict_station = []
        for line in lines:
            polygon = eval(line.polygon)
            line_dict = {
                'id': line.id,
                'company_id': line.company_id,
                'name': line.name,
                'polygon': polygon,
                'color': line.color,
                'stations': [station.to_station_dict() for station in line.stations]
            }
            line_dict_station.append(line_dict)
        return line_dict_station

    def to_join_company_line_dict(self):
        """companies, linesが結合されたテーブルの辞書変換関数

        companiesテーブルとlinesテーブルが結合された
        Stationオブジェクトを辞書型に変換する関数

        Returns:
            辞書型: 下記の辞書が返される
        """
        station_dict = {
            'id': self.id,
            'company_id': self.company_id,
            'name': self.name,
            'address': self.address,
            'prefecture_id': self.prefecture_id,
            'city_code': self.city_code,
            'place_id': self.place_id,
            'geohash': self.geohash,
            'lat': self.lat,
            'lng': self.lng,
            'search_text': self.search_text,
            'lines': self.to_line_dict(self.lines),
            'company': self.company.to_company_dict()
        }
        return station_dict

    def to_line_dict(self, lines):
        """結合のないlinesテーブルの辞書変換関数

        Stationオブジェクトを辞書型に変換する関数

        Args:
            lines (:obj:Line[]): Lineオブジェクトのリスト

        Returns:
            辞書型: 下記の辞書が返される

        """
        line_dict_station = []
        for line in lines:
            line_dict = {
                'id': line.id,
                'company_id': line.company_id,
                'name': line.name,
                'color': line.color,
            }
            line_dict_station.append(line_dict)
        return line_dict_station

    def to_station_dict(self):
        """結合のないstationsテーブルの辞書変換関数

        Stationオブジェクトを辞書型に変換する関数

        Returns:
            辞書型: 下記の辞書が返される

        """
        station_dict = {
            'id': self.id,
            'company_id': self.company_id,
            'name': self.name,
            'address': self.address,
            'prefecture_id': self.prefecture_id,
            'city_code': self.city_code,
            'place_id': self.place_id,
            'geohash': self.geohash,
            'lat': self.lat,
            'lng': self.lng,
            'search_text': self.search_text,
        }
        return station_dict


class Prefecture(Base):
    """Prefectureテーブルクラス

    prefecturesテーブルのカラムの定義
    オブジェクトを辞書変換する関数の定義

    Attributes:
        id (str): 都道府県コード
        name (str): 都道府県名
        lat (float): 都道府県の緯度
        lng (float): 都道府県の緯度
        created_at (timestamp): レコード作成時間
        updated_at (timestamp): レコード更新時間
        cities (:obj:City): citiesテーブル(OneToMany)
        stations (:obj:Station): stationsテーブル(OneToMany)
        spots (:obj:Spot): spotsテーブル(OneToMany)
    """

    # テーブル名
    __tablename__ = 'prefectures'

    # 個々のカラムを定義
    id = Column(String(3), nullable=False, index=True, primary_key=True)
    name = Column(String(20))
    lat = Column(Float)
    lng = Column(Float)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    cities = relationship(
        'City',
        backref='prefectures',
    )
    stations = relationship(
        'Station',
        backref='prefectures',
    )
    spots = relationship('Spot', backref='prefectures')

    def to_join_city_spot_dict(self):
        prefecture_dict = {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lng': self.lng,
            'cities': self.to_city_spot_dict(self.cities)
        }
        return prefecture_dict

    def to_city_spot_dict(self, cities):
        city_dict_list = []
        for city in cities:
            city_dict = {
                'id': city.id,
                'prefecture_id': city.prefecture_id,
                'name': city.name,
                'lat': city.lat,
                'lng': city.lng,
                'spots': self.to_spot_dict(city.spots)
            }
            city_dict_list.append(city_dict)
        return city_dict_list

    def to_spot_dict(self, spots):
        spot_dict_list = []
        for spot in spots:
            spot_dict = {
                'id': spot.id,
                'prefecture_id': spot.prefecture_id,
                'city_code': spot.city_code,
                'name': spot.name,
                'lat': spot.lat,
                'lng': spot.lng,
            }
            spot_dict_list.append(spot_dict)
        return spot_dict_list

    def to_prefecture_dict(self):
        prefecture_dict = {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lng': self.lng,
        }
        return prefecture_dict

    def validate(self):
        column_dict_list = [
            {'column': 'id', 'value': self.id, 'type': str, 'check': 'len', 'num': 3, 'required': True},
            {'column': 'name', 'value': self.name, 'type': str, 'check': '', 'required': True},
            {'column': 'lat', 'value': self.lat, 'type': float, 'check': '', 'required': True},
            {'column': 'lng', 'value': self.lng, 'type': float, 'check': '', 'required': True},
        ]
        for column_dict in column_dict_list:
            validation = validate_type(column_dict)
            if not validation['status']:
                return validation
        if len(self.id) >= 4:
            return {'status': False, 'message': 'id must be less than 3 characters'}
        if self.name[-1] not in ['都', '道', '府', '県']:
            return {'status': False, 'message': 'last character must be one of these 「都」,「道」,「府」,「県」'}
        if 20 > self.lat and self.lat > 46:
            return {'status': False, 'message': 'lat must be between 20 and 46'}
        if not 122 > self.lng and self.lng > 154:
            return {'status': False, 'message': 'lng must be between 122 and 154'}
        return {'status': True}

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
    polygons = Column(LONGTEXT)
    layouts = Column(LONGTEXT)
    columns = Column(LONGTEXT)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
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

    def to_join_spot_town_station_company_line_dict(self):
        spots = [spot.to_spot_dict() for spot in self.spots] if self.spots else []
        towns = [town.to_town_dict() for town in self.towns] if self.towns else []
        stations = [station.to_join_company_line_station_dict() for station in self.stations] if self.stations else []
        city_dict = {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lng': self.lng,
            'layouts': eval(self.layouts),
            'columns': eval(self.columns),
            'facility': self.facility.to_facility_dict(),
            'occupation': self.occupation.to_occupation_dict(),
            'population': self.population.to_population_dict(),
            'spots': spots,
            'towns': towns,
            'stations': stations
        }
        return city_dict

    def to_city_dict(self):
        city_dict = {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lng': self.lng,
            'layouts': eval(self.layouts),
            'columns': eval(self.columns),
        }
        return city_dict

class Facility(Base):
    """
    Facilityテーブルクラス
    """

    # テーブル名
    __tablename__ = 'facilities'

    # 個々のカラムを定義
    id = Column(BIGINT, primary_key=True)
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
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    city = relationship('City')


    def to_facility_dict(self):
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
    id = Column(BIGINT, primary_key=True)
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
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    city = relationship('City')

    def to_occupation_dict(self):
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
    id = Column(BIGINT, primary_key=True)
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
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    city = relationship('City')

    def to_population_dict(self):
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
    Spotテーブルクラス
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
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    city = relationship('City')

    def to_join_city_dict(self):
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
            'city': self.to_city_dict(self.city)
        }
        return spot_dict

    def to_city_dict(self, city):
        city_dict = {
            'id': city.id,
            'name': city.name,
            'lat': city.lat,
            'lng': city.lng,
        }
        return city_dict

    def to_spot_dict(self):
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
    id = Column(BIGINT, primary_key=True)
    prefecture_id = Column(String(3), ForeignKey('prefectures.id'))
    city_code = Column(String(6), ForeignKey('cities.id'))
    name = Column(String(20))
    address = Column(String(100))
    count = Column(Integer)
    count_ratio = Column(Float)
    geohash = Column(String(10))
    lat = Column(Float)
    lng = Column(Float)
    layouts = Column(LONGTEXT)
    columns = Column(LONGTEXT)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def to_short_town_dict(self):
        town_dict = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'prefecture_id': self.prefecture_id,
            'city_code': self.city_code,
            'lat': self.lat,
            'lng': self.lng,
            'geohash': self.geohash,
        }
        return town_dict

    def to_town_dict(self):
        layouts = eval(self.layouts) if self.layouts else ''
        columns = eval(self.columns) if self.columns else ''
        town_dict = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'prefecture_id': self.prefecture_id,
            'city_code': self.city_code,
            'lat': self.lat,
            'lng': self.lng,
            'geohash': self.geohash,
            'count': self.count,
            'count_ratio': self.count_ratio,
            'layouts': layouts,
            'columns': columns,
        }
        return town_dict

def change_time(time):
    added_timezone = time + timedelta(hours=9)
    return added_timezone.strftime('%Y/%m/%d %H:%M:%S')

def validate_type(column_dict):
    if type(column_dict['value']) == column_dict['type']:
        if column_dict['required']:
            if column_dict['value']:
                return {'status': True, 'message': ''}
            else:
                return {'status': False, 'message': f'{column_dict["column"]} is required'}
        return {'status': True, 'message': ''}
    else:
        return {'status': False, 'message': f'{column_dict["column"]} must be {"integer" if column_dict["type"] == int else "float" if column_dict["type"] == float else "string"}'}
