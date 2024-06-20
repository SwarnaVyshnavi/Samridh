from django.db import models
from django.utils import timezone
# Create your models here.

class OrganizationHeads(models.Model):
    id = models.AutoField(primary_key = True)
    firstname = models.CharField(max_length = 25)
    lastname = models.CharField(max_length = 25)
    profile_photo = models.ImageField(upload_to='unverified_organizations/', default='unverified_organizations/Manager/dp.jpg')
    email = models.EmailField(max_length = 254, unique = True)
    phone_number = models.CharField(max_length=10, unique = True)


class UnverifiedOrganizations(models.Model):

    id = models.AutoField(primary_key = True)
    registration_number = models.CharField(max_length = 20, unique = True)
    profile_photo = models.ImageField(upload_to='unverified_organizations/', default='unverified_organizations/Org_dp.jpg')
    certificate = models.FileField(upload_to='unverified_organizations/certificates/', null=True, blank=True)
    email = models.EmailField(max_length=254, unique = True)
    phone_number = models.CharField(max_length=10, unique = True)
    name = models.CharField(max_length = 100)
    Type = models.CharField(max_length = 50, default = '')
    address = models.CharField(max_length = 100)
    state = models.CharField(max_length = 30)
    pincode = models.CharField(max_length = 7)
    password = models.CharField(max_length = 150, default = '')
    head_id = models.ForeignKey("OrganizationHeads" , on_delete=models.CASCADE)

class VerifiedOrganizations(models.Model):

    id = models.AutoField(primary_key = True)
    registration_number = models.CharField(max_length = 20, unique = True)
    profile_photo = models.ImageField(upload_to='verified_organizations/', default='verified_organizations/Org_dp.jpg')
    certificate = models.FileField(upload_to='verified_organizations/certificate/', null=True, blank=True)
    email = models.EmailField(max_length=254, unique = True)
    phone_number = models.CharField(max_length=10, unique = True)
    name = models.CharField(max_length = 100)
    Type = models.CharField(max_length=50, default = '')
    address = models.CharField(max_length = 100)
    state = models.CharField(max_length = 30)
    pincode = models.CharField(max_length = 7)
    password = models.CharField(max_length = 150, default = '')
    head_id = models.ForeignKey("OrganizationHeads" , on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, auto_now = False)
    amount = models.IntegerField(default=0)

class OrganizationStatistics(models.Model):

    id = models.AutoField(primary_key = True)
    organization_id = models.ForeignKey("VerifiedOrganizations", on_delete=models.CASCADE)
    number_of_girls = models.IntegerField(default = 0)
    number_of_boys = models.IntegerField(default = 0)
    number_of_men = models.IntegerField(default = 0)
    number_of_women = models.IntegerField(default = 0)
    expenditure = models.IntegerField(default = 0)


class OrganizationProfile(models.Model):

    id = models.AutoField(primary_key = True)
    organization_id = models.ForeignKey("VerifiedOrganizations", on_delete=models.CASCADE)
    fields = models.JSONField(default=dict)
