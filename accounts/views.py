from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Account
from envelopes.models import Envelope
from transactions.models import Transaction

class IndexView(LoginRequiredMixin, generic.ListView):
  login_url = '/login/'
  template_name = 'accounts/index.html'
  context_object_name = 'all_accounts'

  def get_queryset(self):
    return Account.objects.filter(user_id=self.request.user.id).order_by('name')

  def get_context_data(self, **kwargs):
    context = super(IndexView, self).get_context_data(**kwargs)
    context['all_envelopes'] = Envelope.objects.order_by('name')
    return context

class DetailView(LoginRequiredMixin, generic.DetailView):
  login_url = '/login/'
  model = Account
  template_name = 'accounts/detail.html'

  def get_context_data(self, **kwargs):
    user_id = self.request.user.id
    context = super(DetailView, self).get_context_data(**kwargs)
    context['all_accounts'] = Account.objects.filter(user_id=user_id).order_by('name')
    context['all_envelopes'] = Envelope.objects.order_by('name')
    return context

@login_required
def create_transaction(request):
  account = get_object_or_404(Account, pk=request.POST['account_id'])
  envelope = get_object_or_404(Envelope, pk=request.POST['envelope_id'])
  amount = request.POST['amount']
  if 'subtract' in request.POST:
    amount = float(amount) * -1.00

  try:
    transaction = Transaction(account=account, envelope=envelope, date=request.POST['date'], amount=amount)
  except (KeyError):
    messages.add_message(request, messages.ERROR, 'Something squiffy happened.')
    return render(request, 'accounts/index.html')
  else:
    transaction.save()
    messages.add_message(request, messages.SUCCESS, 'Transaction added.')
    return HttpResponseRedirect(reverse('accounts:detail', args=(account.id,)))
