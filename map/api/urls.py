from django.urls import path
from map.api.views.wikipedia import WikiAPI
from map.api.views.yahoo import (
    ReverseGeocodeAPI
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
    path('search-by-reverse-geocode/', ReverseGeocodeAPI.as_view(), name="reverse-geocode"),
    path('twitter/', TwitterAPI.as_view(), name="twitter"),
    path('event/', EventAPI.as_view(), name="event"),
]