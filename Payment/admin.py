from django.contrib import admin

# Register your models here.
from .models import Donations

class NameDonations(admin.ModelAdmin):
    list_display = [f.name for f in Donations._meta.fields]

admin.site.register(Donations, NameDonations)