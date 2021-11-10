from django.urls import path
from user.api.views import (
    AccountAPI,
    UserAPI
)

urlpatterns = [
    path('', UserAPI.as_view(), name="wiki"),
    path('account/', AccountAPI.as_view(), name="wiki"),
    path('account/logout/', AccountAPI.logout, name="wiki"),
]