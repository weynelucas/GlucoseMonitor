from django.db import models
from django.contrib.auth.models import User

class GlucoseMeasure(models.Model):
    value = models.DecimalField(null=False, blank=False, max_digits=5, decimal_places=2)
    datetime = models.DateTimeField(null=False, blank=False)
    notes = models.CharField(null=True, blank=True, max_length=140)
    user = models.ForeignKey(User, null=False, blank=False)
