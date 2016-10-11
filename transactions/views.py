from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Transaction
from accounts.models import Account
from envelopes.models import Envelope

class IndexView(generic.ListView):
    template_name = 'transactions/index.html'
    context_object_name = 'all_transactions'

    def get_queryset(self):
        return Transaction.objects.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['all_accounts'] = Account.objects.order_by('name')
        context['all_envelopes'] = Envelope.objects.order_by('name')
        return context

def create(request):
    account = get_object_or_404(Account, pk=request.POST['account_id'])
    envelope = get_object_or_404(Envelope, pk=request.POST['envelope_id'])
    try:
        transaction = Transaction(account=account, envelope=envelope, date=request.POST['date'], amount=request.POST['amount'])
    except (KeyError):
        return render(request, 'transactions/index.html', {'message': 'Something squiffy happened.'})
    else:
        transaction.save()
        return HttpResponseRedirect(reverse('transactions:index'))
    return True
