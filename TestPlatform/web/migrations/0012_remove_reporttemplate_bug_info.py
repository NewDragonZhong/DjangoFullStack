# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-13 07:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_reporttemplate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporttemplate',
            name='bug_info',
        ),
    ]
