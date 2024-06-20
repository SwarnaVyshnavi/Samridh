from django.db import models

# Create your models here.

class Manager(models.Model):

    id =models.AutoField(primary_key = True)
    email = models.EmailField( max_length=254, unique = True)
    photo = models.ImageField(upload_to='Admin/', default='Admin/dp.jpg')
    phone_number = models.CharField(max_length=10, unique = True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    password = models.CharField(max_length=200)

