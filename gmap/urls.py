from django.contrib import admin
from . import views
from django.urls import (
    path,
    include,
)
from django.conf.urls import url


urlpatterns = [
    #urlがadmin、accounts、mapから始まるもの以外は全てindex.htmlを返す
    url(r'^(?!admin|api).*', views.index, name='index'),
    # url(r'^(?!admin|api).*', views.index, name='index'),
    path('api/', include('map.api.urls')),
    path('admin/', admin.site.urls),
]
