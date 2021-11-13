from django.urls import path
from user.api.views import (
    AuthenticationAPI,
    UserAPI,
)

urlpatterns = [
    path('', UserAPI.as_view(), name="user"),
    path('login/', AuthenticationAPI.login, name="login"),
    path('auth/', AuthenticationAPI.authentication, name="authentication"),
    path('logout/', AuthenticationAPI.logout, name="logout"),
]