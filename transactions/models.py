from django.db import models
from accounts.models import Account
from envelopes.models import Envelope

class Transaction(models.Model):
    account  = models.ForeignKey(Account, on_delete=models.CASCADE)
    envelope = models.ForeignKey(Envelope, on_delete=models.CASCADE)
    date     = models.DateField()
    amount   = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    def __str__(self):
      return self.date.isoformat()
