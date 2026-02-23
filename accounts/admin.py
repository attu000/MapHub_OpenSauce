from django.contrib import admin
from . import models 

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id','username')
    list_display_links = ('id','username')
admin.site.register(models.CustomUser, CustomUserAdmin)