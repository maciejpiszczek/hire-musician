from django.contrib import admin
from . import models


admin.site.register(models.Job)
admin.site.register(models.StudioSession)
admin.site.register(models.Concert)
admin.site.register(models.Tour)
