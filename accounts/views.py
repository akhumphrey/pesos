from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Account
from .forms import AccountForm
from envelopes.models import Envelope
from transactions.models import Transaction

class IndexView(LoginRequiredMixin, generic.ListView):
  template_name = 'accounts/index.html'
  context_object_name = 'all_accounts'

  def get_queryset(self):
    return Account.objects.filter(user_id=self.request.user.id).order_by('name')

  def get_context_data(self, **kwargs):
    context = super(IndexView, self).get_context_data(**kwargs)
    context['all_envelopes'] = Envelope.objects.filter(user_id=self.request.user.id).order_by('name')
    return context

class DetailView(LoginRequiredMixin, generic.DetailView):
  model = Account
  template_name = 'accounts/detail.html'

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
    context['all_accounts'] = Account.objects.filter(user_id=user_id).order_by('name')
    context['all_envelopes'] = Envelope.objects.filter(user_id=user_id).order_by('name')
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

@login_required
def new(request):
  context = {
    'title': 'new account',
    'form': AccountForm(),
  }
  return render(request, 'accounts/new.html', context)

@login_required
def create(request):
  form = AccountForm(request.POST)
  if form.is_valid():
    account = Account.objects.create(name=request.POST.get('name'), user_id=request.user.id)
    messages.add_message(request, messages.SUCCESS, account.name + ' created.')
    return HttpResponseRedirect(reverse('accounts:detail', args=(account.id,)))
  else:
    context = {
      'title': 'new account',
      'form': form,
    }
    messages.add_message(request, messages.ERROR, 'Something squiffy happened.')
    return render(request, 'accounts/new.html', context)

@login_required
def edit(request, account_id):
  try:
    account = Account.objects.get(pk=account_id, user_id=request.user.id)
  except:
    raise Http404('Not found')

  title   = ' '.join(['editing', account.name ])
  form    = AccountForm(instance=account)
  context = {
    'title': title,
    'account': account,
    'form': form,
  }
  return render(request, 'accounts/edit.html', context)

@login_required
def update(request, account_id):
  try:
    account = Account.objects.get(pk=account_id, user_id=request.user.id)
  except:
    raise Http404('Not found')

  form = AccountForm(request.POST)
  if form.is_valid():
    account.name = request.POST.get('name', account.name)
    account.save()
    messages.add_message(request, messages.SUCCESS, account.name + ' updated.')
    return HttpResponseRedirect(reverse('accounts:detail', args=(account.id,)))
  else:
    title = ' '.join(['editing', account.name ])
    context = {
      'title': title,
      'account': account,
      'form': form,
    }
    messages.add_message(request, messages.ERROR, 'Something squiffy happened.')
    return render(request, 'accounts/edit.html', context)
