# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-08 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0012_auto_20160227_2120'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='structure',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='function',
            name='sector',
        ),
        migrations.AlterField(
            model_name='function',
            name='category',
            field=models.IntegerField(blank=True, choices=[(0, 'Jeune'), (1, 'Responsable'), (2, 'Membre associé')], null=True, verbose_name='Categorie'),
        ),
    ]
