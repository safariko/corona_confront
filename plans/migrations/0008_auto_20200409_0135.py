# Generated by Django 2.2.12 on 2020-04-09 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0007_auto_20200409_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='insurance_exists',
            field=models.CharField(choices=[('INSURED', 'Insured'), ('UNINSURED', 'Uninsured')], default='UNINSURED', max_length=9),
        ),
    ]