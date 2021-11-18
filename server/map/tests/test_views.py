import unittest
from map.api.views.views import (
    TwitterAPI,
    CompanyAPI,
    PrefectureCityAPI,
    PrefectureAPI,
    SpotAPI,
    StationAPI,
    LineAPI,
    CityAPI,
    SearchStationAPI,
    SearchTownAPI,
    TableAPI,
)
from django.test import RequestFactory

class TestViews(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_twitter_view(self):
        request = self.factory.get('/api/map/twitter/')
        response = TwitterAPI.as_view()(request)
        self.assertEqual(response.status_code, 404)
        request = self.factory.get('/api/map/twitter/?name=新宿')
        response = TwitterAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_company_view(self):
        request = self.factory.get('/api/map/company/')
        response = CompanyAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_prefecture_city_view(self):
        request = self.factory.get('/api/map/prefecture/city/')
        response = PrefectureCityAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_spot_view(self):
        request = self.factory.get('/api/map/prefecture/city/')
        response = SpotAPI.as_view()(request)
        self.assertEqual(response.status_code, 404)
        request = self.factory.get('/api/map/prefecture/city/?id=1')
        response = SpotAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_prefecture_view(self):
        request = self.factory.get('/api/map/prefecture/')
        response = PrefectureAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_station_view(self):
        request = self.factory.get('/api/map/station/')
        response = StationAPI.as_view()(request)
        self.assertEqual(response.status_code, 404)
        request = self.factory.get('/api/map/station/?prefecture_id=13')
        response = StationAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)
        request = self.factory.get('/api/map/station/?prefecture_id=13&name=新宿駅')
        response = StationAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_line_view(self):
        request = self.factory.get('/api/map/line/')
        response = LineAPI.as_view()(request)
        self.assertEqual(response.status_code, 404)
        request = self.factory.get('/api/map/line/?prefecture_id=13')
        response = LineAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_city_view(self):
        request = self.factory.get('/api/map/city/')
        response = CityAPI.as_view()(request)
        self.assertEqual(response.status_code, 404)
        request = self.factory.get('/api/map/city/?city_code=13101')
        response = CityAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_station_view(self):
        request = self.factory.get('/api/map/search/station/?word=新宿区　ＪＲ')
        response = SearchStationAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_town_view(self):
        request = self.factory.get('/api/map/search/town/?word=新宿区　西')
        response = SearchTownAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_table_view(self):
        request = self.factory.get('/api/map/search/table/')
        response = TableAPI.as_view()(request)
        self.assertEqual(response.status_code, 200)
