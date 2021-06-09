
from django.contrib import admin
from django.urls import path
from .views import CustomUserCreate, CustomUserAPI

app_name = 'users'
urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name="create_user"),
    path('', CustomUserAPI.as_view(), name="list-user"),
]
