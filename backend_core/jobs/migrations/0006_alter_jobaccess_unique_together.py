# Generated by Django 4.1 on 2022-12-30 18:21

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0005_job_is_available'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='jobaccess',
            unique_together={('candidate', 'job')},
        ),
    ]
