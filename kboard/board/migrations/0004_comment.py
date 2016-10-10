# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-10 10:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_auto_20161008_0753'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='board.Post')),
            ],
        ),
    ]
