from django.conf.urls import url

from . import views

app_name = 'transactions'
urlpatterns = [
  url(r'^$', views.IndexView.as_view(), name='index'),
  url(r'^create/$', views.create, name='create'),
]
