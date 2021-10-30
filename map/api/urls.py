from django.urls import path
from map.api.views.wikipedia import WikiAPI
from map.api.views.yahoo import (
    ReverseGeocodeAPI,
    PlaceInfoAPI
)
from map.api.views.views import (
    TwitterAPI,
    EventAPI,
    HouseModel,
    CompanyAPI,
    PrefectureCityAPI,
    PrefectureAPI,
    SpotAPI,
    StationAPI,
    LineAPI,
    CityAPI
)
# from map.api.views import (
#     WikiAPI,
#     ReverseGeocodeAPI,
#     EventAPI
# )

urlpatterns = [
    path('wiki/',WikiAPI.as_view(), name="wiki"),
    path('twitter/', TwitterAPI.as_view(), name="twitter"),
    path('event/', EventAPI.as_view(), name="event"),
    path('search-by-reverse-geocode/', ReverseGeocodeAPI.as_view(), name="reverse-geocode"),
    path('search-by-place-info/', PlaceInfoAPI.as_view(), name="place-info"),
    path('house-model/', HouseModel.as_view(), name="house-model"),
    path('company/', CompanyAPI.as_view(), name="company"),
    path('prefecture/city/', PrefectureCityAPI.as_view(), name="prefecture"),
    path('spot/', SpotAPI.as_view(), name="spot"),
    path('station/', StationAPI.as_view(), name="station"),
    path('line/', LineAPI.as_view(), name="line"),
    path('prefecture/', PrefectureAPI.as_view(), name="prefecture-station"),
    path('city/', CityAPI.as_view(), name="city"),
]