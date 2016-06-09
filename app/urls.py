# app/urls.py

from django.conf.urls import url

from app import views

urlpatterns = [

	url(r'^$', views.repos, name='profile'),
	url(r'^commits/$', views.topten, name="commits"),
	url(r'^nodata/$', views.topten, name="nodata"),
]