# Generated by Django 4.1 on 2022-10-13 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_jobaccess'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='days_off',
            field=models.PositiveIntegerField(default=0),
        ),
    ]