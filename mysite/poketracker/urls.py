from django.conf.urls import url

from . import views

app_name = 'poketracker'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^caught/$', views.CaughtView.as_view(), name='caught'),
    url(r'^uncaught/$', views.UncaughtView.as_view(), name='uncaught'),
    url(r'^evolve-new/$', views.EvolveNewView.as_view(), name='evolve-new'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
]
