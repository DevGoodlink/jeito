# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 16:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0010_auto_20170122_1908'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agreement',
            options={'get_latest_by': 'date', 'verbose_name': 'Convention'},
        ),
        migrations.AddField(
            model_name='payment',
            name='scan',
            field=models.FileField(blank=True, upload_to='paiements', verbose_name='Scan'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='signed_agreement',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='signedx_booking', to='booking.Agreement', verbose_name='N° convention signée'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='signed_agreement_scan',
            field=models.FileField(blank=True, upload_to='conventions_signees', verbose_name='Scan convention signée'),
        ),
    ]
