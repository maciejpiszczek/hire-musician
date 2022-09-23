from django.db import models
from .models import PrivateMessage
import django_filters


class PrivMessagesFilter(django_filters.FilterSet):
    class Meta:
        model = PrivateMessage
        fields = ['sender', 'receiver']
        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': '',
                },
            }
        }
