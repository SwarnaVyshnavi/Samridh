from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from Payment.models import Donations
from .models import VerifiedOrganizations, UnverifiedOrganizations, OrganizationHeads, OrganizationStatistics, OrganizationProfile

####

from django.db.models import Sum
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def editSection(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        section_name = request.POST.get('section_name')
        section_description = request.POST.get('section_description')

        registration_number = request.POST.get('reg_no')

        new_data = {section_name : section_description}  

        data_prev = OrganizationProfile.objects.get(organization_id = registration_number)
        data = data_prev.fields
        data_dict = json.loads(data)

        data_dict[section_name] = section_description

        modified_data = json.dumps(data_dict)

        data_prev.fields = modified_data
        data_prev.save()
        # For demonstration, let's assume the section was edited successfully
        print(section_name, section_description)
        success = True
        
        return JsonResponse({'success': success})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
def addSection(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':

        section_name = request.POST.get('section_name')
        section_description = request.POST.get('section_description')
        registration_number = request.POST.get('reg_no')


        print(section_name, section_description, request.POST.get('reg_no'))
  
        new_data = {section_name : section_description}  

        data_prev = OrganizationProfile.objects.get(organization_id = registration_number) 
        data = data_prev.fields

        data_dict = json.loads(data)

        data_dict.update(new_data)

        modified_data = json.dumps(data_dict)

        data_prev.fields = modified_data
        data_prev.save()

        success = True
        
        return JsonResponse({'success': success})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'})



def ProfileView(request):
    # return HttpResponse('<h1>Hello</h1>')

    if 'Auth' in request.session :

        org = VerifiedOrganizations.objects.get(id = request.session['id'])
        head = org.head_id

        stats = OrganizationStatistics.objects.get(organization_id = request.session['id'])

        info = OrganizationProfile.objects.get(organization_id = request.session['id'])
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
            donations = Donations.objects.filter(organization_id = request.session['id'])[:3]
        except :

            donations = ''

        request.session['user'] = context

    else : 
        return HttpResponse('<h1> Session expired.. Login again </h1>')

    top_donors = Donations.objects.filter(organization_id=request.session['id']).values('amount', 'donor_name').annotate(total_amount=Sum('amount')).order_by('-total_amount')[:3]

    # Iterate over top_donors to calculate the total donations for each donor
    for donor in top_donors:
        donor['total'] = Donations.objects.filter(organization_id = request.session['id'], donor_name=donor['donor_name']).aggregate(total=Sum('amount'))['total']

    return render(request, 'Org_dashboard.html',{"donations" : donations, 'topdonors' : top_donors, 'fields' : fields})

def ComplaintView(request):

    return render(request, 'Org_complaint.html')

def DonationView(request):

    if 'Auth' in request.session :
        
        donations = Donations.objects.filter(organization_id = request.session['id']).all()

        if donations.exists():

            return render(request, 'Org_donation.html',{'donations' : donations})
        else:
            # donations = ''
            return render(request, 'Org_donation.html',{'donations' : donations})

    return HttpResponse('<h1> Session expired.. Login again </h1>')