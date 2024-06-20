from django.contrib import admin

from .models import *

class NameUnverified(admin.ModelAdmin):
    list_display = [f.name for f in UnverifiedOrganizations._meta.fields]

class NameVerified(admin.ModelAdmin):
    list_display = [f.name for f in VerifiedOrganizations._meta.fields]

class NameStats(admin.ModelAdmin):
    list_display = [f.name for f in OrganizationStatistics._meta.fields]

class NameManager(admin.ModelAdmin):
    list_display = [f.name for f in OrganizationHeads._meta.fields]

class NameOrganizationProfile(admin.ModelAdmin):
    list_display = [f.name for f in OrganizationProfile._meta.fields]

admin.site.register(OrganizationProfile, NameOrganizationProfile)
admin.site.register(UnverifiedOrganizations, NameUnverified)
admin.site.register(VerifiedOrganizations, NameVerified)
admin.site.register(OrganizationHeads, NameManager)
admin.site.register(OrganizationStatistics, NameStats)
