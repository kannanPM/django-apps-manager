from django.conf.urls import url
from django.urls import include, path

from django.contrib import admin
from django.contrib.auth import views as auth_views

from main.views import Home, Subscribe


urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$',Home.logout, name='logout'),
    url(r'^home/$',Home.home, name='home'),
    url(r'^subscribe/$',Subscribe.as_view(), name='subscribe'),
    url(r'^subscribetoapp/$',Subscribe.subscribetoapp, name='subscribe'),
    url(r'^getstat/$',Home.getstat, name='getstat'),
    url(r'^info/$',Subscribe.info, name='subscribe'),
    path('openapp/<int:appid>',Home.openapp, name='app'),
]
