from django.urls import path
from map.api.views import (
    GeocodeAPI,
    ReverseGeocodeAPI,
    StationAPI,
    StationDetailAPI,
    LineAPI,
    WikiAPI,
    CompanyAPI,
    CSVCompanyAPI
)
from . import views
urlpatterns = [
    path('search-by-geocode', GeocodeAPI.as_view(), name="geocode"),
    path('search-by-reverse-geocode', ReverseGeocodeAPI.as_view(), name="reverse-geocode"),
    path("station/",StationAPI.as_view(), name="station"),
    path("station/line/",StationDetailAPI.as_view(), name="station-line"),
    path("station/polygon/",LineAPI.as_view(), name="station-polygon"),
    path("",CompanyAPI.as_view(), name="station-polygon"),
    path("station/line/wiki/",WikiAPI.as_view(), name="wiki"),
    path("download/<str:filename>",views.download),
    path("practice/",views.practice),
    path("csv/",CSVCompanyAPI.as_view()),
]
