from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from envelopes import views as envelope_views
from transactions import views as transaction_views

urlpatterns = [
  url(r'^login/$', auth_views.login, {'template_name': 'shared/login.html'}, name='login'),
  url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name='logout'),
  url(r'^accounts/', include('accounts.urls')),
  url(r'^accounts', account_views.IndexView.as_view(), name='accounts'),
  url(r'^envelopes/', include('envelopes.urls')),
  url(r'^envelopes', envelope_views.IndexView.as_view(), name='envelopes'),
  url(r'^transactions/', include('transactions.urls')),
  url(r'^transactions', transaction_views.IndexView.as_view(), name='transactions'),
  url(r'^admin/', admin.site.urls),
  url(r'^home/', include('home.urls')),
  url(r'^', include('home.urls')),
]
