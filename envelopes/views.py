from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Envelope
from .forms import EnvelopeForm
from accounts.models import Account
from transactions.models import Transaction

class IndexView(LoginRequiredMixin, generic.ListView):
  template_name       = 'envelopes/index.html'
  context_object_name = 'all_envelopes'

  def get_queryset(self):
    return Envelope.objects.filter(user_id=self.request.user.id).order_by('name')

  def get_context_data(self, **kwargs):
    context = super(IndexView, self).get_context_data(**kwargs)
    context['all_accounts']          = Account.objects.filter(user_id=self.request.user.id).order_by('name')
    context['envelope_budget_total'] = 0.0
    context['remaining_total']       = 0.0

    all_envelopes = self.get_queryset()
    for envelope in all_envelopes:
      context['envelope_budget_total'] = context['envelope_budget_total'] + float(envelope.monthly_budget)
      context['remaining_total']       = context['remaining_total'] + float(envelope.running_total())

    return context

class DetailView(LoginRequiredMixin, generic.DetailView):
  model         = Envelope
  template_name = 'envelopes/detail.html'

  def get(self, request, *args, **kwargs):
    try:
      self.object = self.get_object()
    except:
      raise Http404('Not found')

    if self.object.user_id != request.user.id:
      raise Http404('Not found')

    context = self.get_context_data(object=self.object)
    return self.render_to_response(context)

  def get_context_data(self, **kwargs):
    user_id = self.request.user.id
    context = super(DetailView, self).get_context_data(**kwargs)
    context['all_accounts']  = Account.objects.filter(user_id=user_id).order_by('name')
    context['all_envelopes'] = Envelope.objects.filter(user_id=user_id).order_by('name')
    return context

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
      return HttpResponseRedirect(reverse('envelopes:index'))

  else:
    all_envelopes = Envelope.objects.all()
    try:
      count = Envelope.refill(request.POST['date'], account, all_envelopes, amount, False)
    except ValueError as e:
      messages.add_message(request, messages.ERROR, str(e))
      return HttpResponseRedirect(reverse('envelopes:index'))

  if count == 1:
    plural = 'transaction'
  else:
    plural = 'transactions'

  messages.add_message(request, messages.SUCCESS, 'Refill successful - ' + str(count) + ' ' + plural + ' added.')
  return HttpResponseRedirect(reverse('envelopes:index'))

@login_required
def edit(request, envelope_id):
  try:
    envelope = Envelope.objects.get(pk=envelope_id, user_id=request.user.id)
  except:
    raise Http404('Not found')

  title    = ' '.join(['editing', envelope.name ])
  form     = EnvelopeForm(instance=envelope)
  context  = {
    'title': title,
    'envelope': envelope,
    'form': form,
  }
  return render(request, 'envelopes/edit.html', context)

@login_required
def update(request, envelope_id):
  try:
    envelope = Envelope.objects.get(pk=envelope_id, user_id=request.user.id)
  except:
    raise Http404('Not found')

  form = EnvelopeForm(request.POST)
  if form.is_valid():
    envelope.name           = request.POST.get('name', envelope.name)
    envelope.monthly_budget = request.POST.get('monthly_budget', envelope.monthly_budget)
    if request.POST.get('immutable_budget', False):
      envelope.immutable_budget = True
    else:
      envelope.immutable_budget = False
    envelope.save()
    messages.add_message(request, messages.SUCCESS, envelope.name + ' updated.')
    return HttpResponseRedirect(reverse('envelopes:detail', args=(envelope.id,)))
  else:
    title = ' '.join(['editing', envelope.name ])
    context = {
      'title': title,
      'envelope': envelope,
      'form': form,
    }
    messages.add_message(request, messages.ERROR, 'Something squiffy happened.')
    return render(request, 'envelopes/edit.html', context)
