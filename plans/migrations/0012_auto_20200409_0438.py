# Generated by Django 2.2.12 on 2020-04-09 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0011_auto_20200409_0414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='insurance_no',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='insurance_yes',
        ),
    ]