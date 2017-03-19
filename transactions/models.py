from django.db import models
from accounts.models import Account

class Transaction(models.Model):
  account  = models.ForeignKey(Account, on_delete=models.CASCADE)
  envelope = models.ForeignKey('envelopes.Envelope', on_delete=models.CASCADE, null=True, default=None)
  date     = models.DateField()
  amount   = models.DecimalField(default=0, max_digits=8, decimal_places=2)

  class Meta:
    ordering = ['-date']

  def __str__(self):
    return self.date.isoformat()

  def save(self, *args, **kwargs):
    result = super(Transaction, self).save(*args, **kwargs)
    if self.envelope:
      self.envelope.calculate_transaction_velocity()

    return result
