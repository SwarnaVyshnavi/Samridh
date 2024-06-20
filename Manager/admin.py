from django.contrib import admin

# Register your models here.
from .models import Manager

class NameManager(admin.ModelAdmin):
    list_display = [f.name for f in Manager._meta.fields]

admin.site.register(Manager, NameManager)