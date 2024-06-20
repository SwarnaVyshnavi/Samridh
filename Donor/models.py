from django.db import models


class Donors(models.Model):

    id =models.AutoField(primary_key = True)
    email = models.EmailField( max_length=254, unique = True)
    profile_photo = models.ImageField(upload_to='Donor/', default='dp.jpg')
    phone_number = models.CharField(max_length=10, unique = True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    
