from django.db import models
from decimal import Decimal

class Envelope(models.Model):
    name           = models.CharField(max_length=50)
    monthly_budget = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    def __str__(self):
      return self.name

    def running_total(self):
      if self.transaction_set.count() < 1:
        return self.monthly_budget

      total = 0
      for transaction in self.transaction_set.all():
        total = total - ( -1 * Decimal(transaction.amount) )

      return total
