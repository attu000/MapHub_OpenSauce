from django.contrib import admin
from . import models

admin.site.register(models.Site)
admin.site.register(models.Map)
admin.site.register(models.Content)
admin.site.register(models.LiketoSite)