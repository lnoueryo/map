from django.urls import path
from management.api.views import (
    CompanyAPI,
    LineAPI,
    StationAPI,
    CSVCompanyAPI
)
from . import views
urlpatterns = [
    path('company/',CompanyAPI.as_view(), name="company"),
    path('company/csv/',CSVCompanyAPI.as_view(), name="csv_company"),
    path('line/',LineAPI.as_view(), name="line"),
    path('station/',StationAPI.as_view(), name="line"),
]
