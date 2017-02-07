# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 20:38
from __future__ import unicode_literals

from django.db import migrations, models


def forward(apps, schema_editor):
    Entry = apps.get_model('accounting', 'Entry')
    for entry in Entry.objects.all():
        if entry.amount > 0:
            entry.revenue = entry.amount
        if entry.amount < 0:
            entry.expense = -entry.amount
        entry.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0004_auto_20170207_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='comment',
            field=models.CharField(max_length=1000, verbose_name='Commentaire', blank=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='expense',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Dépense'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entry',
            name='revenue',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Recette'),
            preserve_default=False,
        ),
        migrations.RunPython(forward),
    ]
