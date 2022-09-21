import os

from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')

    Group.objects.create(name=os.environ.get("DJ_GROUP_MUSICIANS"))


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_userprofile_slug'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]
