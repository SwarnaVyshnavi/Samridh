from django.shortcuts import render, redirect
from datetime import date

from django.contrib.auth.hashers import check_password, make_password
from .models import *

# from Organization.models import VerifiedOrganizations, UnverifiedOrganizations, OrganizationHeads
from Organization.models import VerifiedOrganizations, UnverifiedOrganizations, OrganizationHeads, OrganizationStatistics, OrganizationProfile


from Payment.models import Donations

## Mail sender

from django.core.mail import send_mail
from django.conf import settings


def send_email(request):

    subject = request.Content['subject']
    message = request.Content['message']

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [request.Content['receiver']]
    
    send_mail(subject, message, from_email, recipient_list)
    # return render(request,'Home.html')


def Manager_Home(request):

    Count={
        "unverified_count" : UnverifiedOrganizations.objects.count(),
        "Verified_count" : VerifiedOrganizations.objects.count(),
        'amount' : UnverifiedOrganizations.objects.count(),
        'donations' : Donations.objects.all().order_by('-date')
    }

    return render(request,'Manager_home.html',{'Count':Count})


def unverified(request):

    organizations = UnverifiedOrganizations.objects.all()
    return render(request, 'Unverified_list.html', {'organizations':organizations})



def delete_organization(request,id):
    org = UnverifiedOrganizations.objects.get(id = id)
    org_head = org.head_id  
    org_head.delete()
    return redirect('Manager:unverified')


def change_to_verified(request,id):
    message = {}

    unverified_organization = UnverifiedOrganizations.objects.get(id = id)
        
    verified_organization = VerifiedOrganizations.objects.create(

        registration_number=unverified_organization.registration_number,
        profile_photo=unverified_organization.profile_photo,
        certificate=unverified_organization.certificate,
        email=unverified_organization.email,
        phone_number=unverified_organization.phone_number,
        name=unverified_organization.name,
        Type=unverified_organization.Type,
        address=unverified_organization.address,
        state=unverified_organization.state,
        pincode=unverified_organization.pincode,
        password=unverified_organization.password,
        head_id=unverified_organization.head_id

    )
    data1 = OrganizationStatistics.objects.create(
        organization_id = verified_organization
    )
    data2 = OrganizationProfile.objects.create(
        organization_id = verified_organization
    )
    # print("enter")
    data1.save()
    data2.save()
    # Content ={
    #         'subject' : "Application Accepted",
    #         'message' : "We have verified your application. Login with your credentials to complete your profile🙂.",
    #         'receiver': unverified_organization.email,
    # }
    request.Content=Content
    send_mail(
            'Application Accepted',
            'We have verified your application. Login with your credentials to complete your profile🙂.',
            settings.EMAIL_HOST,
            [email],
            fail_silently=False,
    )

    message={
        'message' : True
    }

    # Delete the record from UnverifiedOrganizations
    unverified_organization.delete()

    
    return redirect('Manager:unverified')
    # except:
    #     print("Error")

    # return render(request,'Unverified_list.html',message)
    


def view_more(request,id):

    organization = UnverifiedOrganizations.objects.filter(id = id)

    if organization.exists():
        organization = UnverifiedOrganizations.objects.get(id = id)
    else:
        organization = VerifiedOrganizations.objects.get(id = id)        
    return render(request, 'Unverified_organization.html', {'organization' : organization})


def Verified_Organizations(request):
    organizations = VerifiedOrganizations.objects.all()
    return render(request, 'organizations_list.html', {'organizations':organizations})

