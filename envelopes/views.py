from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Envelope

def index(request):
    all_envelopes = Envelope.objects.order_by('name')
    context = {'all_envelopes': all_envelopes}
    return render(request, 'envelopes/index.html', context)

def detail(request, envelope_id):
    envelope = get_object_or_404(Envelope, pk=envelope_id)
    return render(request, 'envelopes/detail.html', {'envelope': envelope})
