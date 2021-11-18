#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Modelのテストモジュール

mapで定義されているModelのテスト用モジュール

"""

import unittest

from django.conf import settings
from sqlalchemy import *
from sqlalchemy.orm import *

from map.models import *

engine = settings.ENGINE

class CompanyModelTests(unittest.TestCase):
    """CompanyModelのテストクラス

    CompanyクラスのCRUDとModelに記載されている辞書型へ
    変換する関数の動作確認


    """
    def setUp(self):
        """create関数

        companiesテーブルにレコード作成

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        company = Company()
        company.name = '鉄道会社井上'
        company.address = '東京都世田谷区松原1-43-14'
        company.founded = '1990年9月8日'
        company.created_at = '2021-06-12 04:36:28'
        company.updated_at = '2021-06-12 04:36:28'
        session.add(company)
        session.commit()
        session.close()

    def test_update(self):
        """update関数

        setUpで作成されたレコードを更新

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        company = session.query(Company).filter(Company.name=='鉄道会社井上').first()
        company.address = '東京都世田谷区松原'
        session.commit()
        session.close()
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        company = session.query(Company).filter(Company.name=='鉄道会社井上').first()
        self.assertEqual(company.address, '東京都世田谷区松原')
        session.close()

    def test_to_company_dict(self):
        """to_company_dict関数の動作確認関数

        辞書型へ変換する関数to_company_dict()
        の動作と辞書内のキー確認

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        company = session.query(Company).filter(Company.id==1).first()
        values = list(company.to_company_dict().keys())
        needed_columns = ['id', 'name', 'address', 'founded']
        self.assertTrue(values == needed_columns)
        session.close()

    def test_to_join_line_station_dict(self):
        """to_join_line_station_dict関数の動作確認関数

        辞書型へ変換する関数to_join_line_station_dict()
        の動作、その関数内で使用されている関数の動作と
        辞書内のキー確認

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        company = session.query(Company).filter(Company.id==1).first()
        company_dict = company.to_join_line_station_dict()
        company_values = list(company_dict.keys())
        needed_company_columns = ['id', 'name', 'address', 'founded', 'lines']
        self.assertTrue(company_values == needed_company_columns)
        line_dict = company_dict['lines'][0]
        line_values = list(line_dict.keys())
        needed_line_columns = ['id', 'name', 'polygon', 'color', 'stations']
        self.assertTrue(line_values == needed_line_columns)
        station_dict = line_dict['stations'][0]
        station_values = list(station_dict.keys())
        needed_station_columns = ['id', 'name', 'lat', 'lng']
        self.assertTrue(station_values == needed_station_columns)
        session.close()

    def tearDown(self):
        """delete関数

        setUpで作成されたレコード削除

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        session.query(Company).filter(Company.name=='鉄道会社井上').delete()
        session.commit()
        session.close()

# class LineModelTests(unittest.TestCase):
#     """LineModelのテストクラス

#     LineクラスのCRUDとModelに記載されている辞書型へ
#     変換する関数の動作確認


#     """
#     def setUp(self):
#         """create関数

#         linesテーブルにレコード作成

#         """
#         Session = scoped_session(sessionmaker(bind=engine))
#         session = Session()
#         line = Line()
#         line.name = '井上線'
#         line.company_id = 1
#         line.founded = '1990年9月8日'
#         line.created_at = '2021-06-12 04:36:28'
#         line.updated_at = '2021-06-12 04:36:28'
#         session.add(line)
#         session.commit()
#         session.close()

#     def test_update(self):
#         """update関数

#         setUpで作成されたレコードを更新

#         """
#         Session = scoped_session(sessionmaker(bind=engine))
#         session = Session()
#         line = session.query(Line).filter(Line.name=='鉄道会社井上').first()
#         line.address = '東京都世田谷区松原'
#         session.commit()
#         session.close()
#         Session = scoped_session(sessionmaker(bind=engine))
#         session = Session()
#         line = session.query(Line).filter(Line.name=='鉄道会社井上').first()
#         self.assertEqual(line.address, '東京都世田谷区松原')
#         session.close()

#     def test_to_line_dict(self):
#         """to_line_dict関数の動作確認関数

#         辞書型へ変換する関数to_line_dict()
#         の動作と辞書内のキー確認

#         """
#         Session = scoped_session(sessionmaker(bind=engine))
#         session = Session()
#         line = session.query(Line).filter(Line.id==1).first()
#         values = list(line.to_line_dict().keys())
#         needed_columns = ['id', 'name', 'address', 'founded']
#         for needed_column in needed_columns:
#             self.assertIn(needed_column, values)
#         session.close()

#     def test_to_join_line_station_dict(self):
#         """to_join_line_station_dict関数の動作確認関数

#         辞書型へ変換する関数to_join_line_station_dict()
#         の動作、その関数内で使用されている関数の動作と
#         辞書内のキー確認

#         """
#         Session = scoped_session(sessionmaker(bind=engine))
#         session = Session()
#         line = session.query(Line).filter(Line.id==1).first()
#         line_dict = line.to_join_line_station_dict()
#         line_values = list(line_dict.keys())
#         needed_line_columns = ['id', 'name', 'address', 'founded', 'lines']
#         for needed_line_column in needed_line_columns:
#             self.assertIn(needed_line_column, line_values)
#         line_dict = line_dict['lines'][0]
#         line_values = list(line_dict.keys())
#         needed_line_columns = ['id', 'name', 'polygon', 'color', 'stations']
#         for needed_line_column in needed_line_columns:
#             self.assertIn(needed_line_column, line_values)
#         station_dict = line_dict['stations'][0]
#         station_values = list(station_dict.keys())
#         needed_station_columns = ['id', 'name', 'lat', 'lng']
#         for needed_station_column in needed_station_columns:
#             self.assertIn(needed_station_column, station_values)
#         session.close()

#     def tearDown(self):
#         """delete関数

#         setUpで作成されたレコード削除

#         """
#         Session = scoped_session(sessionmaker(bind=engine))
#         session = Session()
#         session.query(Line).filter(Line.name=='鉄道会社井上').delete()
#         session.commit()
#         session.close()

class PrefectureModelTests(unittest.TestCase):
    """PrefectureModelのテストクラス

    PrefectureクラスのCRUDとModelに記載されている辞書型へ
    変換する関数の動作確認


    """
    def setUp(self):
        """create関数

        prefecturesテーブルにレコード作成

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        prefecture = Prefecture()
        prefecture.id = '48'
        prefecture.name = '井上県'
        prefecture.lat = 40.6813
        prefecture.lng = 140.767
        prefecture.created_at = '2021-06-12 04:36:28'
        prefecture.updated_at = '2021-06-12 04:36:28'
        session.add(prefecture)
        session.commit()
        session.close()

    def test_update(self):
        """update関数

        setUpで作成されたレコードを更新

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        prefecture = session.query(Prefecture).filter(Prefecture.name=='井上県').first()
        prefecture.lat = 30.3594
        session.commit()
        session.close()
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        prefecture = session.query(Prefecture).filter(Prefecture.name=='井上県').first()
        self.assertEqual(prefecture.lat, 30.3594)
        session.close()

    def test_to_join_city_spot_dict(self):
        """to_join_city_spot_dict関数の動作確認関数

        辞書型へ変換する関数to_join_city_spot_dict)
        の動作、その関数内で使用されている関数の動作と
        辞書内のキー確認

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        prefecture = session.query(Prefecture).filter(Prefecture.id=='13').first()
        prefecture_dict = prefecture.to_join_city_spot_dict()
        prefecture_values = list(prefecture_dict.keys())
        needed_prefecture_columns = ['id', 'name', 'lat', 'lng', 'cities']
        for prefecture_value in prefecture_values:
            self.assertIn(prefecture_value, needed_prefecture_columns)
        city_dict = prefecture_dict['cities'][0]
        city_values = list(city_dict.keys())
        needed_city_columns = ['id', 'prefecture_id', 'name', 'lat', 'lng', 'spots']
        for city_value in city_values:
            self.assertIn(city_value, needed_city_columns)
        spot_dict = city_dict['spots'][0]
        spot_values = list(spot_dict.keys())
        needed_spot_columns = ['id', 'prefecture_id', 'city_code', 'name', 'lat', 'lng']
        for spot_value in spot_values:
            self.assertIn(spot_value, needed_spot_columns)
        session.close()

    def test_to_prefecture_dict(self):
        """to_prefecture_dict関数の動作確認関数

        辞書型へ変換する関数to_company_dict()
        の動作と辞書内のキー確認

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        prefecture = session.query(Prefecture).filter(Prefecture.id=='13').first()
        values = list(prefecture.to_prefecture_dict().keys())
        needed_columns = ['id', 'name', 'lat', 'lng']
        for needed_column in needed_columns:
            self.assertIn(needed_column, values)
        session.close()

    def tearDown(self):
        """delete関数

        setUpで作成されたレコード削除

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        session.query(Prefecture).filter(Prefecture.name=='井上県').delete()
        session.commit()
        session.close()

class CityModelTests(unittest.TestCase):
    """CityModelのテストクラス

    CityクラスのCRUDとModelに記載されている辞書型へ
    変換する関数の動作確認


    """
    def setUp(self):
        """create関数

        Citiesテーブルにレコード作成

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        city = City()
        city.id = '48101'
        city.prefecture_id = '13'
        city.name = '井上市'
        city.lat = 40.6813
        city.lng = 140.767
        city.polygons = ''
        city.layouts = ''
        city.columns = ''
        city.created_at = '2021-06-12 04:36:28'
        city.updated_at = '2021-06-12 04:36:28'
        session.add(city)
        session.commit()
        session.close()

    def test_update(self):
        """update関数

        setUpで作成されたレコードを更新

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        city = session.query(City).filter(City.name=='井上市').first()
        city.lat = 30.3594
        session.commit()
        session.close()
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        city = session.query(City).filter(City.name=='井上市').first()
        self.assertEqual(city.lat, 30.3594)
        session.close()

    def test_to_join_spot_town_station_company_line_dict(self):
        """to_join_spot_town_station_company_line_dict関数の動作確認関数

        辞書型へ変換する関数to_join_spot_town_station_company_line_dict()
        の動作、その関数内で使用されている関数の動作と
        辞書内のキー確認

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        city = session.query(City).filter(City.id=='13101').first()
        city_dict = city.to_join_spot_town_station_company_line_dict()
        city_values = list(city_dict.keys())
        needed_city_columns = ['id', 'name', 'lat', 'lng', 'layouts', 'columns', 'facility', 'occupation', 'population', 'spots', 'towns', 'stations']
        self.assertTrue(set(city_values) == set(needed_city_columns))
        session.close()

    def test_to_city_dict(self):
        """to_city_dict関数の動作確認関数

        辞書型へ変換する関数to_company_dict()
        の動作と辞書内のキー確認

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        city = session.query(City).filter(City.id=='13101').first()
        values = list(city.to_city_dict().keys())
        needed_columns = ['id', 'name', 'lat', 'lng']
        self.assertTrue(set(values) == set(needed_columns))
        session.close()

    def tearDown(self):
        """delete関数

        setUpで作成されたレコード削除

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        session.query(City).filter(City.name=='井上市').delete()
        session.commit()
        session.close()

class SpotModelTests(unittest.TestCase):
    """SpotModelのテストクラス

    SpotクラスのCRUDとModelに記載されている辞書型へ
    変換する関数の動作確認


    """
    def setUp(self):
        """create関数

        spotsテーブルにレコード作成

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        spot = Spot()
        spot.prefecture_id = '13'
        spot.city_code = '13101'
        spot.name = '井上公園'
        spot.lat = 40.6813
        spot.lng = 140.767
        spot.place_id = '12345678912345689'
        spot.address = ''
        spot.geohash = ''
        spot.created_at = '2021-06-12 04:36:28'
        spot.updated_at = '2021-06-12 04:36:28'
        session.add(spot)
        session.commit()
        session.close()

    def test_update(self):
        """update関数

        setUpで作成されたレコードを更新

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        spot = session.query(Spot).filter(Spot.name=='井上公園').first()
        spot.lat = 30.3594
        session.commit()
        session.close()
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        spot = session.query(Spot).filter(Spot.name=='井上公園').first()
        self.assertEqual(spot.lat, 30.3594)
        session.close()

    def test_to_join_city_dict(self):
        """to_join_city_dict関数の動作確認関数

        辞書型へ変換する関数to_join_city_dict()
        の動作、その関数内で使用されている関数の動作と
        辞書内のキー確認

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        spot = session.query(Spot).filter(Spot.id==1).first()
        spot_dict = spot.to_join_city_dict()
        spot_values = list(spot_dict.keys())
        needed_spot_columns = ['id', 'name', 'prefecture_id', 'city_code', 'lat', 'lng', 'place_id', 'address', 'geohash', 'city']
        self.assertTrue(set(spot_values) == set(needed_spot_columns))
        session.close()

    def test_to_spot_dict(self):
        """to_spot_dict関数の動作確認関数

        辞書型へ変換する関数to_spot_dict()
        の動作と辞書内のキー確認

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        spot = session.query(Spot).filter(Spot.id=='1').first()
        values = list(spot.to_spot_dict().keys())
        needed_columns = ['id', 'prefecture_id', 'city_code', 'name', 'place_id', 'address', 'geohash', 'lat', 'lng']
        self.assertTrue(set(values) == set(needed_columns))
        session.close()

    def tearDown(self):
        """delete関数

        setUpで作成されたレコード削除

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        session.query(Spot).filter(Spot.name=='井上公園').delete()
        session.commit()
        session.close()

class TownModelTests(unittest.TestCase):
    """STownModelのテストクラス

    TownクラスのCRUDとModelに記載されている辞書型へ
    変換する関数の動作確認


    """
    def setUp(self):
        """create関数

        townsテーブルにレコード作成

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        town = Town()
        town.prefecture_id = '13'
        town.city_code = '13101'
        town.name = '井上町'
        town.lat = 40.6813
        town.lng = 140.767
        town.address = ''
        town.geohash = ''
        town.created_at = '2021-06-12 04:36:28'
        town.updated_at = '2021-06-12 04:36:28'
        town.count = 0
        town.count_ratio = 0
        town.layouts = ''
        town.columns = ''
        session.add(town)
        session.commit()
        session.close()

    def test_update(self):
        """update関数

        setUpで作成されたレコードを更新

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        town = session.query(Town).filter(Town.name=='井上町').first()
        town.lat = 30.3594
        session.commit()
        session.close()
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        town = session.query(Town).filter(Town.name=='井上町').first()
        self.assertEqual(town.lat, 30.3594)
        session.close()

    def test_to_short_town_dict(self):
        """to_short_town_dict関数の動作確認関数

        辞書型へ変換する関数to_short_town_dict()
        の動作、その関数内で使用されている関数の動作と
        辞書内のキー確認

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        town = session.query(Town).filter(Town.id==1).first()
        town_dict = town.to_short_town_dict()
        town_values = list(town_dict.keys())
        needed_town_columns = ['id', 'name', 'city_code', 'lat', 'lng', 'prefecture_id', 'address', 'geohash']
        self.assertTrue(set(town_values) == set(needed_town_columns))
        session.close()

    def test_to_town_dict(self):
        """to_town_dict関数の動作確認関数

        辞書型へ変換する関数to_town_dict()
        の動作と辞書内のキー確認

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        town = session.query(Town).filter(Town.id==1).first()
        values = list(town.to_town_dict().keys())
        needed_columns = ['id', 'prefecture_id', 'city_code', 'name', 'address', 'geohash', 'lat', 'lng', 'count', 'count_ratio', 'layouts', 'columns']
        self.assertTrue(set(values) == set(needed_columns))
        session.close()

    def tearDown(self):
        """delete関数

        setUpで作成されたレコード削除

        """
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        session.query(Town).filter(Town.name=='井上町').delete()
        session.commit()
        session.close()
