from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Envelope

class IndexView(generic.ListView):
    template_name = 'envelopes/index.html'
    context_object_name = 'all_envelopes'

    def get_queryset(self):
        return Envelope.objects.order_by('name')

class DetailView(generic.DetailView):
    model = Envelope
    template_name = 'envelopes/detail.html'
