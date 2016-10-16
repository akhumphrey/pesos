from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Envelope
from accounts.models import Account
from transactions.models import Transaction

class IndexView(generic.ListView):
  template_name = 'envelopes/index.html'
  context_object_name = 'all_envelopes'

  def get_queryset(self):
    return Envelope.objects.order_by('name')

  def get_context_data(self, **kwargs):
    context = super(IndexView, self).get_context_data(**kwargs)
    context['all_accounts'] = Account.objects.order_by('name')
    context['envelope_budget_total'] = 0.0
    context['remaining_total'] = 0.0

    all_envelopes = self.get_queryset()
    for envelope in all_envelopes:
      context['envelope_budget_total'] = context['envelope_budget_total'] + float(envelope.monthly_budget)
      context['remaining_total'] = context['remaining_total'] + float(envelope.running_total())

    return context

class DetailView(generic.DetailView):
  model = Envelope
  template_name = 'envelopes/detail.html'

  def get_context_data(self, **kwargs):
    context                  = super(DetailView, self).get_context_data(**kwargs)
    context['all_accounts']  = Account.objects.order_by('name')
    context['all_envelopes'] = Envelope.objects.order_by('name')
    return context

def create_transaction(request):
  account  = get_object_or_404(Account, pk=request.POST['account_id'])
  envelope = get_object_or_404(Envelope, pk=request.POST['envelope_id'])
  amount   = float(request.POST['amount'])
  if 'subtract' in request.POST:
    amount = amount * -1.00

  try:
    transaction = Transaction(account=account, envelope=envelope, date=request.POST['date'], amount=amount)
  except (KeyError):
    return render(request, 'envelopes/index.html', {'message': 'Something squiffy happened.'})
  else:
    transaction.save()
    return HttpResponseRedirect(reverse('envelopes:detail', args=(envelope.id,)))
