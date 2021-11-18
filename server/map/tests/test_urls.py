import unittest
from django.urls import reverse, resolve
from map.api.views.wikipedia import WikiAPI
from map.api.views.yahoo import (
    ReverseGeocodeAPI,
    PlaceInfoAPI
)
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
    EventAPI,
)

class TestUrls(unittest.TestCase):
    def test_reverse_geocode_url(self):
        url = reverse('reverse-geocode')
        self.assertEquals(resolve(url).func.view_class, ReverseGeocodeAPI)
    def test_place_info_url(self):
        url = reverse('place-info')
        self.assertEquals(resolve(url).func.view_class, PlaceInfoAPI)
    def test_twitter_url(self):
        url = reverse('twitter')
        self.assertEquals(resolve(url).func.view_class, TwitterAPI)
    def test_company_url(self):
        url = reverse('company')
        self.assertEquals(resolve(url).func.view_class, CompanyAPI)
    def test_prefecture_city_url(self):
        url = reverse('prefecture-city')
        self.assertEquals(resolve(url).func.view_class, PrefectureCityAPI)
    def test_prefecture_url(self):
        url = reverse('prefecture')
        self.assertEquals(resolve(url).func.view_class, PrefectureAPI)
    def test_spot_url(self):
        url = reverse('spot')
        self.assertEquals(resolve(url).func.view_class, SpotAPI)
    def test_station_url(self):
        url = reverse('station')
        self.assertEquals(resolve(url).func.view_class, StationAPI)
    def test_line_url(self):
        url = reverse('line')
        self.assertEquals(resolve(url).func.view_class, LineAPI)
    def test_city_url(self):
        url = reverse('city')
        self.assertEquals(resolve(url).func.view_class, CityAPI)
    def test_search_station_url(self):
        url = reverse('search-station')
        self.assertEquals(resolve(url).func.view_class, SearchStationAPI)
    def test_search_spot_url(self):
        url = reverse('search-town')
        self.assertEquals(resolve(url).func.view_class, SearchTownAPI)
    def test_search_table_url(self):
        url = reverse('table')
        self.assertEquals(resolve(url).func.view_class, TableAPI)