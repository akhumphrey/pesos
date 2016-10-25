from django.forms import ModelForm
from .models import Envelope

class EnvelopeForm(ModelForm):
  class Meta:
    model = Envelope
    fields = ['name', 'monthly_budget', 'immutable_budget']
