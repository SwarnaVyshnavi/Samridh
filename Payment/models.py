from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from Organization.models import VerifiedOrganizations

# Create your models here.


class Donations(models.Model):

    id = models.AutoField(primary_key = True)
    organization_id = models.ForeignKey("Organization.VerifiedOrganizations", on_delete=models.CASCADE)
    organization_name = models.CharField(max_length = 100, default = '')
    organization_type= models.CharField( max_length=50, default = 'Orphanage')
    donor_id = models.ForeignKey("Donor.Donors", on_delete=models.CASCADE)
    donor_name = models.CharField(max_length = 100, default = '')
    amount = models.IntegerField()
    transaction_id = models.CharField( max_length=200, unique = True)
    message = models.CharField( max_length=200, default = '')
    date = models.DateField(auto_now_add=True)


@receiver(post_save, sender=Donations)
def update_verified_organization_amount(sender, instance, created, **kwargs):
    if created:
        # Increment the amount field of the related VerifiedOrganizations instance
        organization = instance.organization_id
        organization.amount += instance.amount
        organization.save()
