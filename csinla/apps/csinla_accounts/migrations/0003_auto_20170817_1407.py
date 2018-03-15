# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-17 06:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csinla_accounts', '0002_auto_20170811_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='newstudentsubmission',
            name='is_valid',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u6709\u6548'),
        ),
        migrations.AlterField(
            model_name='newstudentcomment',
            name='belong',
            field=models.CharField(choices=[('hd', 'LA\u996e\u98df\u5a31\u4e50\u54a8\u8be2'), ('jj', '\u5165\u5b66\u4e0e\u9009\u8bfe\u6307\u5357'), ('rx', '\u65b0\u95fb\u8d44\u8baf'), ('jz', '\u9a7e\u7167\u4e0e\u4ea4\u901a')], default='jj', max_length=8, verbose_name='\u6240\u5c5e\u6a21\u5757'),
        ),
        migrations.AlterField(
            model_name='newstudentsubmission',
            name='belong',
            field=models.CharField(choices=[('hd', 'LA\u996e\u98df\u5a31\u4e50\u54a8\u8be2'), ('jj', '\u5165\u5b66\u4e0e\u9009\u8bfe\u6307\u5357'), ('rx', '\u65b0\u95fb\u8d44\u8baf'), ('jz', '\u9a7e\u7167\u4e0e\u4ea4\u901a')], default='jj', max_length=8, verbose_name='\u6240\u5c5e\u6a21\u5757'),
        ),
        migrations.AlterField(
            model_name='submissionpicture',
            name='image',
            field=models.ImageField(blank=True, upload_to='house/%Y/%m', verbose_name='\u56fe\u7247'),
        ),
    ]
