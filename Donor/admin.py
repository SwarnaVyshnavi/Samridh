from django.contrib import admin

# Register your models here.
from .models import Donors

class NameDonor(admin.ModelAdmin):
    list_display = [f.name for f in Donors._meta.fields]

admin.site.register(Donors, NameDonor)