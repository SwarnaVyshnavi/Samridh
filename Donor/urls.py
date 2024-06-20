from django.urls import path 

from .views import *

app_name = 'Donor'

urlpatterns = [
    
    path('Profile/', DonorProfileView, name = 'Donor-Profile'),
    path('My_Donations/', DonorDonationView, name = 'Donations'),
    # path('Exit/', Exit, name = 'Exit'),
#     path('Organization/<int:id>/', DonorOrganizationView, name = 'Organization'),
]