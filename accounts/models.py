from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
  user    = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
  name    = models.CharField(max_length=50)
  balance = models.DecimalField(default=0, max_digits=8, decimal_places=2)

  def __str__(self):
    return self.name
