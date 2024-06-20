from django.shortcuts import render
from .models import Donors
from Payment.models import Donations
# def DonorOrganizationView(request,id):
#     pass

# def DonorOrganizationSearchView(request):
#     pass

base_template = 'Donor_Base.html'

def DonorProfileView(request):
    if 'Auth' in request.session:
        
        donor = Donors.objects.get( id = request.session.get('id'))
        # print(donor.count())
        return render(request, 'Donor_profile.html', {'donor' : donor, 'base_template' : base_template})

    else:
        return render(request, 'Exit.html')
    
    # return render(request, 'Donor_profile.html', {})

def DonorDonationView(request):
    if 'Auth' in request.session:
        
        donations = Donations.objects.filter( donor_id = request.session.get('id'))
        print(request.session.get('id'))
        # print(donor.count())
        return render(request, 'Donor_donations.html', {'donations' : donations, 'base_template' : base_template})

    else:
        return render(request, 'Exit.html')
    
    # return render(request, 'Donor_profile.html', {})

