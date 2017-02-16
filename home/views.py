from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
  return render(request, 'home/index.html', {'title':'home'})
