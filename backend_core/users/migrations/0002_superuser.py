# Generated by Django 4.1 on 2022-08-03 21:25
import os

from django.contrib.auth import get_user_model
from django.db import migrations


def create_superuser(apps, schema_editor):
    User = apps.get_model('users', 'CustomUser')

    DJ_SU_USERNAME = os.environ.get('DJ_SU_USERNAME')
    DJ_SU_EMAIL = os.environ.get('DJ_SU_EMAIL')
    DJ_SU_PASSWORD = os.environ.get('DJ_SU_PASSWORD')

    User.objects.create_superuser(
        email=DJ_SU_EMAIL,
        username=DJ_SU_USERNAME,
        password=DJ_SU_PASSWORD
    )


def delete_superuser(apps, schema_editor):
    User = apps.get_model('users', 'CustomUser')
    admin = User.objects.get(pk=1)
    if admin.is_superuser:
        admin.delete()
    else:
        raise IndexError('User with id = 1 is not an admin.')


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser)
    ]
