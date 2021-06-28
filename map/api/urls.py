from django.conf.urls import url
from django.urls import path
from . import views
from map.api.views import (
    WikiAPI,
    ReverseGeocodeAPI,
)

urlpatterns = [
    path('station/wiki/',WikiAPI.as_view(), name="wiki"),
    path('search-by-reverse-geocode/', ReverseGeocodeAPI.as_view(), name="reverse-geocode"),
]