from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Transaction

class IndexView(generic.ListView):
    template_name = 'transactions/index.html'
    context_object_name = 'all_transactions'

    def get_queryset(self):
        return Transaction.objects.order_by('-date')
