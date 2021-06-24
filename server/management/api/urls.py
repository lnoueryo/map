from django.urls import path
from management.api.views import (
    CompanyAPI,
    LineAPI,
    StationAPI,
    CSVCompanyAPI,
    CSVLineAPI,
    CSVStationAPI,
    LineStationAPI,
    # LineStationDetailApi
)
from . import views
urlpatterns = [
    path('company/',CompanyAPI.as_view(), name="company"),
    path('company/csv/',CSVCompanyAPI.as_view(), name="csv_company"),
    path('line/',LineAPI.as_view(), name="line"),
    path('line/csv/',CSVLineAPI.as_view(), name="csv_line"),
    path('station/',StationAPI.as_view(), name="station"),
    path('line/station/',LineStationAPI.as_view(), name="line_station"),
    path('station/csv/',CSVStationAPI.as_view(), name="csv_station"),
    # path('line/station/<int:pk>/',LineStationDetailApi.as_view(), name="line_detail"),
]
