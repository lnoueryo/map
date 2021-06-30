from django.urls import path
from map.api.views import (
    WikiAPI,
    ReverseGeocodeAPI,
    EventAPI
)

urlpatterns = [
    path('station/wiki/',WikiAPI.as_view(), name="wiki"),
    path('event/', EventAPI.as_view(), name="event"),
    path('search-by-reverse-geocode/', ReverseGeocodeAPI.as_view(), name="reverse-geocode"),
]