from django.urls import path 
from .views import *

app_name = 'Authentication'

urlpatterns = [
    path('OrganizationLogin', OrganizationLoginView, name = 'Organization-Login'),
    path('OrganizationRegistration', OrganizationRegistrationView, name = 'Organization-Registration'),

    path('DonorLogin',DonorLoginView, name = 'Donor-Login'),
    path('DonorRegistartion', DonorRegistrationView, name = 'Donor-Registration'),

    path('ManagerLogin',ManagerLoginView, name = 'Manager-Login'),
    path('ManagerRegistartion', ManagerRegistrationView, name = 'Manager-Registration'),

    path('Logout', LogoutView, name = 'Logout'),

    # otp 

    path('send_otp/', send_otp, name='send_otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),

]