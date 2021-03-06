# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-28 23:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=5000)),
                ('to_name', models.CharField(choices=[('EM', 'Emily (the brain)'), ('HO', 'Howie (the muscle)')], max_length=2)),
                ('from_name', models.TextField(max_length=200)),
                ('from_email', models.EmailField(max_length=254)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
