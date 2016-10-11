from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Account

class IndexView(generic.ListView):
    template_name = 'accounts/index.html'
    context_object_name = 'all_accounts'

    def get_queryset(self):
        return Account.objects.order_by('name')

class DetailView(generic.DetailView):
    model = Account
    template_name = 'accounts/detail.html'
