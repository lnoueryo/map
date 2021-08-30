from django.contrib import admin
from . import views
from django.urls import (
    path,
    include,
)
from django.conf.urls import url, handler500
from django.views.defaults import server_error
import logging

urlpatterns = [
    #urlがadmin、accounts、mapから始まるもの以外は全てindex.htmlを返す
    url(r'^(?!admin|api).*', views.index, name='index'),
    # url(r'^(?!admin|api).*', views.index, name='index'),
    path('api/', include('map.api.urls')),
    path('admin/', admin.site.urls),
]

def _handler500(request, *arg, **kargs):
    logging.exception