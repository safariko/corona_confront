# Generated by Django 2.2.12 on 2020-04-11 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0004_auto_20200411_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reimburse',
            name='zip_code',
            field=models.IntegerField(),
        ),
    ]