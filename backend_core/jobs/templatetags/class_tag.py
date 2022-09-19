from ..import models

from django import template
register = template.Library()


@register.filter(name='get_class')
def get_class(value):
    if not models.StudioSession.objects.get(slug=value):
        if not models.Concert.objects.get(slug=value):
            if not models.Tour.objects.get(slug=value):
                raise ValueError('Job not found!')
            return models.Tour.objects.get(slug=value).__class__.__name__
        return models.Concert.objects.get(slug=value).__class__.__name__
    return models.StudioSession.objects.get(slug=value).__class__.__name__
