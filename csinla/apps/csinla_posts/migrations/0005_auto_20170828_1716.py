# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-28 09:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('csinla_posts', '0004_auto_20170828_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 27, 9, 16, 38, 688000, tzinfo=utc), verbose_name='\u5230\u671f\u65f6\u95f4'),
        ),
    ]
