# Generated by Django 2.2.12 on 2020-04-08 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0004_auto_20200408_2210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reimburse',
            name='thumb',
        ),
    ]