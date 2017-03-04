from django.conf.urls import url

from . import views

app_name = 'home'
urlpatterns = [
  url(r'^create_transaction/$', views.create_transaction, name='create_transaction'),
  url(r'^refill/$', views.refill, name='refill'),
  url(r'^', views.home, name='home'),
]
