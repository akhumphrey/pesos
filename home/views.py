from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from accounts.models import Account
from envelopes.models import Envelope
from envelopes.forms import EnvelopeForm
from transactions.models import Transaction

@login_required
def home(request):
  context = {
    'title': 'home',
    'all_accounts': Account.objects.filter(user_id=request.user.id).order_by('name'),
    'all_envelopes': Envelope.objects.filter(user_id=request.user.id).order_by('name'),
  }
  return render(request, 'home/index.html', context)

@login_required
def create_transaction(request):
  user_id = request.user.id
  try:
    account  = Account.objects.get(pk=request.POST['account_id'], user_id=user_id)
    envelope = Envelope.objects.get(pk=request.POST['envelope_id'], user_id=user_id)
  except:
    raise Http404('Not found')

  amount = float(request.POST['amount'])
  if 'subtract' in request.POST:
    amount = amount * -1.00

  try:
    transaction = Transaction(account=account, envelope=envelope, date=request.POST['date'], amount=amount)
  except (KeyError):
    messages.add_message(request, messages.ERROR, 'Something squiffy happened.')
    return render(request, 'envelopes/index.html')
  else:
    transaction.save()
    messages.add_message(request, messages.SUCCESS, 'Transaction added.')
    return HttpResponseRedirect(reverse('envelopes:detail', args=(envelope.id,)))

@login_required
def refill(request):
  user_id = request.user.id
  try:
    account = Account.objects.get(pk=request.POST['account_id'], user_id=user_id)
  except:
    raise Http404('Not found')

  amount = float(request.POST['amount'])
  envelope_budget_total           = 0.0
  envelope_immutable_budget_total = 0.0
  immutable_budget_envelopes      = Envelope.objects.filter(user_id=user_id).filter(immutable_budget=True)

  if len(immutable_budget_envelopes):
    for envelope in immutable_budget_envelopes:
      envelope_immutable_budget_total += float(envelope.monthly_budget)

    remaining_envelopes = Envelope.objects.filter(user_id=user_id).filter(immutable_budget=False)
    amount -= envelope_immutable_budget_total

    try:
      count = Envelope.refill(request.POST['date'], account, immutable_budget_envelopes, envelope_immutable_budget_total, True)
      count += Envelope.refill(request.POST['date'], account, remaining_envelopes, amount, False)
    except ValueError as e:
      messages.add_message(request, messages.ERROR, str(e))
      return HttpResponseRedirect(reverse('envelopes'))

  else:
    all_envelopes = Envelope.objects.all()
    try:
      count = Envelope.refill(request.POST['date'], account, all_envelopes, amount, False)
    except ValueError as e:
      messages.add_message(request, messages.ERROR, str(e))
      return HttpResponseRedirect(reverse('envelopes'))

  if count == 1:
    plural = 'transaction'
  else:
    plural = 'transactions'

  messages.add_message(request, messages.SUCCESS, 'Refill successful - ' + str(count) + ' ' + plural + ' added.')
  return HttpResponseRedirect(reverse('envelopes'))
