# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-11 15:26
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_auto_20161008_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=ckeditor.fields.RichTextField(default=''),
        ),
    ]
