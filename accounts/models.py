from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=50)
    balance = models.DecimalField(default=0, max_digits=8, decimal_places=2)
