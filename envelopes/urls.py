from django.conf.urls import url

from . import views

app_name = 'envelopes'
urlpatterns = [
  url(r'^$', views.IndexView.as_view(), name='index'),
  url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
  url(r'^(?P<envelope_id>[0-9]+)/edit/$', views.edit, name='edit'),
  url(r'^(?P<envelope_id>[0-9]+)/update/$', views.update, name='update'),
  url(r'^create_transaction/$', views.create_transaction, name='create_transaction'),
  url(r'^refill/$', views.refill, name='refill'),
]
