from django.urls import path 
from .views import *

app_name = 'Organization'

urlpatterns = [
    path('profile/', ProfileView, name = 'profile'),
    path('donation/', DonationView, name = 'donation'),
    path('complaint/', ComplaintView, name = 'complaint'),
    
    #
    path('edit-section/', editSection, name='edit_section'),
    path('add-section/', addSection, name='add_section'),

]
