# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0005_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar',
            name='dire',
            field=models.CharField(default=b'', max_length=256),
            preserve_default=True,
        ),
    ]
