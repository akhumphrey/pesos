from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Account
from envelopes.models import Envelope
from transactions.models import Transaction

class IndexView(generic.ListView):
    template_name = 'accounts/index.html'
    context_object_name = 'all_accounts'

    def get_queryset(self):
        return Account.objects.order_by('name')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['all_envelopes'] = Envelope.objects.order_by('name')
        return context

class DetailView(generic.DetailView):
    model = Account
    template_name = 'accounts/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['all_accounts'] = Account.objects.order_by('name')
        context['all_envelopes'] = Envelope.objects.order_by('name')
        return context

def create_transaction(request):
    account = get_object_or_404(Account, pk=request.POST['account_id'])
    envelope = get_object_or_404(Envelope, pk=request.POST['envelope_id'])
    try:
        transaction = Transaction(account=account, envelope=envelope, date=request.POST['date'], amount=request.POST['amount'])
    except (KeyError):
        return render(request, 'accounts/index.html', {'message': 'Something squiffy happened.'})
    else:
        transaction.save()
        return HttpResponseRedirect(reverse('accounts:detail', args=(account.id,)))
