from django.urls import path 
from .views import *

app_name = 'Manager'

urlpatterns = [

    ## Manager Dashboard

    path('ManagerProfile',Manager_Home,name='managerprofile'),
    path('unverified',unverified,name='unverified'),
    path('verified_organizations',Verified_Organizations,name='organizations'),

    ## Status update

    path('unverified/delete/<int:id>',delete_organization,name='Delete_entry'),
    path('unverified/update/<int:id>',change_to_verified,name='update'),
    path('unverified/view_more/<int:id>',view_more,name='view_more'),
]