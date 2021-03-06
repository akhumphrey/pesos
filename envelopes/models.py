from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from transactions.models import Transaction
from datetime import datetime, timedelta

class Envelope(models.Model):
  user                 = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
  name                 = models.CharField(max_length=50)
  monthly_budget       = models.DecimalField(default=0, max_digits=8, decimal_places=2)
  immutable_budget     = models.BooleanField(default=True)
  transaction_velocity = models.DecimalField(default=0, max_digits=18, decimal_places=6)

  def __str__(self):
    return self.name

  def running_total(self):
    if self.transaction_set.count() < 1:
      return self.monthly_budget

    total = 0
    for transaction in self.transaction_set.all():
      total = total - ( -1 * Decimal(transaction.amount) )

    return total

  def calculate_transaction_velocity(self):
    if self.transaction_set.count() < 1:
      return 0

    limit    = datetime.now() - timedelta(days=90)
    total    = Transaction.objects.filter(envelope_id=self.id,date__gt=limit).aggregate(models.Sum('amount'))
    velocity = total['amount__sum'] / 90

    self.transaction_velocity = velocity
    self.save()

    return velocity

  @classmethod
  def refill(cls, date, account, envelopes, amount, immutable=None):
    if len(envelopes) < 1:
      raise ValueError('No envelopes to be filled.')

    ratio = 1.0
    total = 0.0

    for envelope in envelopes:
      total += float(envelope.monthly_budget)

    if total > amount:
      if immutable:
        raise ValueError('Not enough funds to refill the given envelopes.')
      else:
        ratio = amount / total

    transactions = 0
    for envelope in envelopes:
      transaction_amount = round(float(envelope.monthly_budget)*ratio, 2)
      if transaction_amount > 0.0:
        amount -= transaction_amount
        transaction = Transaction(account=account, envelope=envelope, date=date, amount=transaction_amount)
        transaction.save()
        transactions += 1

    if amount > 0.0:
      transaction = Transaction(account=account, date=date, amount=round(amount, 2))
      transaction.save()
      transactions += 1

    return transactions
