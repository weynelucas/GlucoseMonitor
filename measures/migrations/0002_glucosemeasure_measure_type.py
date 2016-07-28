# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measures', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='glucosemeasure',
            name='measure_type',
            field=models.CharField(choices=[('FST', 'Em jejum'), ('AFM', 'Após refeição')], default='FST', max_length=3),
        ),
    ]
