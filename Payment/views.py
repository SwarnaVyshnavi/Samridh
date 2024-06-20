from django.shortcuts import render

## Payment logic

import razorpay
from django.conf import settings

from .models import *
from Organization.models import VerifiedOrganizations
from Donor.models import Donors


def payment(request):

    if request.method == 'POST':

        amount = int(request.POST['amount']) * 100

        payment_data = request.session.get('payment_data', {})  # Provide default value as empty dictionary if key doesn't exist

        # Now you can access the values within payment_data
        # For example, if payment_data contains a key called 'amount', you can access its value like this:
        org_id = payment_data.get('org_id')
        print(payment_data)
        org = VerifiedOrganizations.objects.get(id = org_id)

        donor_id = Donors.objects.get(id = request.session.get('id'))

        request.session['org_id'] = org_id
        client = razorpay.Client(auth = (settings.KEY, settings.SECRET) )
        payment = client.order.create({'amount': amount , 'currency' : 'INR', 'payment_capture':'1'})
        data = Donations(amount=amount // 100, transaction_id=payment['id'],message=request.POST.get('message'),
        organization_type=request.POST.get('organization_type'),organization_name=request.POST.get('organization_name'),
        donor_name=request.POST.get('donor_name'),donor_id=donor_id,organization_id=org)
        data.save()
        print(payment)
        return render(request,'payment.html',{'payment':payment})

    return render(request,'payment.html')

def success(request):
    return render(request,'Success.html')


