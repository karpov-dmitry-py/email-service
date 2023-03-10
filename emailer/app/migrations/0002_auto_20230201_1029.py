# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-02-01 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tracking',
            options={'ordering': ['-sent_at'], 'verbose_name': '\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u0440\u0430\u0441\u0441\u044b\u043b\u043a\u0438', 'verbose_name_plural': '\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u0440\u0430\u0441\u0441\u044b\u043b\u043e\u043a'},
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='is_running',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='tracking',
            name='opened_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
