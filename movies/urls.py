from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list$', views.movieList, name='list'),
    url(r'^movie/(?P<movie_pk>\d+)/$', views.movie, name='movie'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^cabinet/(?P<name>\w+)/$', views.cabinet, name='cabinet'),
    url(r'^list/(?P<name>\w+)/$', views.userList, name='userlist'),
    url(r'^list/(?P<name>\w+)/(?P<genre>[a-zA-Z_-]+)/$',
        views.listByGenre,
        name='genrelisted'
    ),
    url(r'^add/(?P<movie_pk>\d+)$', views.add, name='add'),
    url(r'^rate/(?P<movie_pk>\d+)/(?P<name>\w+)/$', views.rate, name='rate')
]
