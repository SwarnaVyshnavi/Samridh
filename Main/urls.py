from django.urls import path 
from .views import LandingPageView, OrganizationSearchView, OrganizationView, InitializeDonation

urlpatterns = [
    path('', LandingPageView, name = 'LandingPage'),
    path('organizations/search/', OrganizationSearchView, name = 'OrganizationSearch'),
    path('Organization/<int:id>/', OrganizationView, name = 'Organization'),
    path('InitDonation/<int:id>/', InitializeDonation, name = 'Init-Donation'),
]