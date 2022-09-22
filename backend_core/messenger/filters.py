from django.db import models
from .models import PrivateMessage
import django_filters


class PrivMessagesFilter(django_filters.FilterSet):
    class Meta:
        model = PrivateMessage
        fields = ['message_text', ]
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }
