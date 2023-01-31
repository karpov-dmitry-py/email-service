from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

urlpatterns = [
    url('admin/', admin.site.urls, name='admin'),
    url('', include('app.urls')),
]
