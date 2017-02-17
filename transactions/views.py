from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Transaction
from accounts.models import Account
from envelopes.models import Envelope

class IndexView(LoginRequiredMixin, generic.ListView):
  template_name = 'transactions/index.html'
  context_object_name = 'all_transactions'

  def get_queryset(self):
    return Transaction.objects.filter(account__user_id=self.request.user.id).order_by('-date')

  def get_context_data(self, **kwargs):
    context = super(IndexView, self).get_context_data(**kwargs)
    context['all_accounts'] = Account.objects.filter(user_id=self.request.user.id).order_by('name')
    context['all_envelopes'] = Envelope.objects.filter(user_id=self.request.user.id).order_by('name')
    return context

@login_required
def create(request):
  account = get_object_or_404(Account, pk=request.POST['account_id'])
  envelope = get_object_or_404(Envelope, pk=request.POST['envelope_id'])
  amount = request.POST['amount']
  if 'subtract' in request.POST:
    amount = float(amount) * -1.00

  try:
    transaction = Transaction(account=account, envelope=envelope, date=request.POST['date'], amount=amount)
  except (KeyError):
    messages.add_message(request, messages.ERROR, 'Something squiffy happened.')
    return render(request, 'transactions/index.html')
  else:
    transaction.save()
    messages.add_message(request, messages.SUCCESS, 'Transaction added.')
    return HttpResponseRedirect(reverse('transactions:index'))
