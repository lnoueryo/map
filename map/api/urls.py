from django.urls import path
from map.api.views.wikipedia import WikiAPI
from map.api.views.yahoo import (
    ReverseGeocodeAPI,
    PlaceInfoAPI
)
from map.api.views.views import (
    TwitterAPI,
    EventAPI
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
]