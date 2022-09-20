from django.db import models
from .models import Job
import django_filters


class JobsFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = ['instrument', 'music_style']
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }
