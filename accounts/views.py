from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Account

def index(request):
    all_accounts = Account.objects.order_by('name')
    context = {'all_accounts': all_accounts}
    return render(request, 'index.html', context)

def detail(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    return render(request, 'detail.html', {'account': account})
