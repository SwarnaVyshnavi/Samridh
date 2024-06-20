from django.urls import path
from .views import *

## payment
app_name = 'Payment'
urlpatterns = [

    path('',payment,name='payment'),
    path('success/',success,name='success'),
]