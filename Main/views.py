from django.shortcuts import render, redirect
from django.db.models import Q
from django.db.models import F, Sum, FloatField, ExpressionWrapper, Q

from Payment.models import Donations
from Organization.models import VerifiedOrganizations, UnverifiedOrganizations, OrganizationHeads, OrganizationStatistics, OrganizationProfile

from django.db.models import Sum
import json
from django.http import JsonResponse
from Donor.models import Donors

def LandingPageView(request):
    
    count = {

        "oldagehomes" : VerifiedOrganizations.objects.filter(Type = 'Old-Age Home').count(),
        "orphnages" : VerifiedOrganizations.objects.filter(Type = 'Orphanage').count(),
        'amount' : Donations.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    }

    sorted_organizations_dict = {}

    orphanages = VerifiedOrganizations.objects.filter(Type='Orphanage').annotate(
        difference=ExpressionWrapper((F('organizationstatistics__expenditure') - F('amount')) * 100 / F('organizationstatistics__expenditure'), output_field=FloatField())
    ).order_by('difference')


    old_age_homes = VerifiedOrganizations.objects.filter(Type='Old-Age Home').annotate(
        difference=ExpressionWrapper((F('organizationstatistics__expenditure') - F('amount')) * 100 / F('organizationstatistics__expenditure'), output_field=FloatField())
    ).order_by('difference')

    sorted_organizations_dict['Orphanages'] = orphanages
    sorted_organizations_dict['OldAgeHomes'] = old_age_homes

    return render(request, 'index.html', {'count' : count, 'list' : sorted_organizations_dict})

def OrganizationSearchView(request):
    base_template = ''
    if 'Auth' in request.session:
        if request.session.get('user_type') == 'Donor':
            base_template = 'Donor_Base.html'
        else:
            base_template = 'Org_Base.html'
    else:
        base_template = 'Base.html'

    print(base_template,'asdfghjkl')
    if request.method == 'POST' :
        Organizations = VerifiedOrganizations.objects.filter(Q(name = request.POST.get('name')))
        print(Organizations.count(),request.POST.get('name'))        

    else :
        Organizations = VerifiedOrganizations.objects.all()

    types = {
        'orphanages' : VerifiedOrganizations.objects.filter(Type = 'Orphanage').count(),
        'oldagehomes' : VerifiedOrganizations.objects.filter(Type = 'Old-Age Home').count()
    }

    return render(request, 'ViewOrganizations/organization_search.html',{"base_template" : base_template, 'Organizations' : Organizations, 'types' : types})

def OrganizationView(request,id):

    base_template = ''
    if 'Auth' in request.session:
        if request.session.get('user_type') == 'Donor':
            base_template = 'Donor_Base.html'
        else:
            base_template = 'Org_Base.html'
    else:
        base_template = 'Base.html'
    print(base_template,'asdfghjkl')

    org = VerifiedOrganizations.objects.get(id = id)
    head = org.head_id

    stats = OrganizationStatistics.objects.get(organization_id = id)

    info = OrganizationProfile.objects.get(organization_id = id)
    # Parse the JSON data from the JSONField
    json_data = info.fields  # Access your JSONField
    fields = json.loads(json_data)  # Parse JSON string to Python dictionary
    
    context = {
        #
        'id' : org.id,
        'registration_number': org.registration_number,
        'org_email': org.email,
        'org_phone_number': org.phone_number,
        'org_name': org.name,
        'org_type': org.Type,
        'org_address': org.address,
        'org_state': org.state,
        'org_pincode': org.pincode,
        'date': org.date.strftime('%Y-%m-%d'),
        #
        'head_firstname': head.firstname,
        'head_lastname': head.lastname,
        'head_email': head.email,
        'head_phone_number': head.phone_number,

        'photo' : org.profile_photo.url,

        'expenditure' : stats.expenditure,
        'women' : stats.number_of_women,
        'men' : stats.number_of_men,
        'boys' : stats.number_of_boys,
        'girls' : stats.number_of_girls,

        #

        'total_amount' : Donations.objects.filter(organization_id = org.id).aggregate(total_amount=Sum('amount'))['total_amount'],
        
    }

    try:      
        donations = Donations.objects.filter(organization_id = org.id)[:3]
    except :

        donations = ''

    # request.session['organization'] = context

    top_donors = Donations.objects.filter(organization_id=org.id).values('amount', 'donor_name').annotate(total_amount=Sum('amount')).order_by('-total_amount')[:3]


    for donor in top_donors:
        donor['total'] = Donations.objects.filter(organization_id =org.id, donor_name=donor['donor_name']).aggregate(total=Sum('amount'))['total']

    return render(request, 'ViewOrganizations/Org_dashboard.html',{"base_template" : base_template, "donations" : donations, 'topdonors' : top_donors, 'fields' : fields,'context':context})



def InitializeDonation(request, id):
    if 'Auth' in request.session:

        org = VerifiedOrganizations.objects.get(id = id)
        donor = Donors.objects.get(id = request.session.get('id'))

        data = {
            'donor' : donor.firstname,
            'org' : org.name,
            'type' : org.Type,
            'org_id' : id
        }

        request.session['payment_data'] = data
        return redirect('Payment:payment')
    else:

        return Httpresponse('<h1>Login to donate.</h1>')