from django.db import models

class Envelope(models.Model):
    name = models.CharField(max_length=50)
    monthly_budget = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    def __str__(self):
      return self.name
