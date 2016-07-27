from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import json

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


class GlucoseMeasure(models.Model):
    value = models.DecimalField(null=False, blank=False, max_digits=5, decimal_places=2)
    datetime = models.DateTimeField(null=False, blank=False)
    notes = models.CharField(null=True, blank=True, max_length=140)
    user = models.ForeignKey(User, null=False, blank=False)
