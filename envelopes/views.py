from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Envelope
from .forms import EnvelopeForm
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

def refill(request):
  account               = get_object_or_404(Account, pk=request.POST['account_id'])
  amount                = float(request.POST['amount'])
  envelope_budget_total = 0.0
  all_envelopes         = Envelope.objects.all()

  for envelope in all_envelopes:
    envelope_budget_total = envelope_budget_total + float(envelope.monthly_budget)

  ratio = 1.0
  if amount < envelope_budget_total:
    ratio = amount / envelope_budget_total

  for envelope in all_envelopes:
    transaction_amount = round(float(envelope.monthly_budget)*ratio, 2)
    if transaction_amount > 0.0:
      amount      = amount - transaction_amount
      transaction = Transaction(account=account, envelope=envelope, date=request.POST['date'], amount=transaction_amount)
      transaction.save()

  if amount > 0.0:
    transaction = Transaction(account=account, envelope=Envelope.objects.get(pk=21), date=request.POST['date'], amount=round(amount, 2))
    transaction.save()

  return HttpResponseRedirect(reverse('envelopes:index'))

def edit(request, envelope_id):
  envelope = get_object_or_404(Envelope, pk=envelope_id)
  title    = ' '.join(['editing', envelope.name ])
  form     = EnvelopeForm(instance=envelope)
  context  = {
    'title': title,
    'envelope': envelope,
    'form': form,
  }
  return render(request, 'envelopes/edit.html', context)

def update(request, envelope_id):
  envelope = get_object_or_404(Envelope, pk=envelope_id)
  form     = EnvelopeForm(request.POST)

  if form.is_valid():
    envelope.name           = request.POST.get('name', envelope.name)
    envelope.monthly_budget = request.POST.get('monthly_budget', envelope.monthly_budget)
    if request.POST.get('immutable_budget', False):
      envelope.immutable_budget = True
    else:
      envelope.immutable_budget = False
    envelope.save()
    return HttpResponseRedirect(reverse('envelopes:detail', args=(envelope.id,)))
  else:
    title = ' '.join(['editing', envelope.name ])
    context = {
      'title': title,
      'envelope': envelope,
      'form': form,
      'message': 'Something squiffy happened.'
    }
    return render(request, 'envelopes/edit.html', context)
