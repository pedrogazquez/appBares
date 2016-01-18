# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0003_category_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bar',
            name='slug',
            field=models.SlugField(default=1992),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bar',
            name='views',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
