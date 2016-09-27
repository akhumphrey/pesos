from django.contrib import admin

from .models import Envelope

class EnvelopeAdmin(admin.ModelAdmin):
    list_display = ('name', 'monthly_budget')

admin.site.register(Envelope, EnvelopeAdmin)
