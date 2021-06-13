from django.urls import path
from management.api.views import (
    CompanyAPI,
)
from . import views
urlpatterns = [
    path('company/',CompanyAPI.as_view(), name="company"),
]
