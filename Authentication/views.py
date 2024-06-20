
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password

from Manager.models import Manager
from Donor.models import Donors
from Organization.models import VerifiedOrganizations, UnverifiedOrganizations, OrganizationHeads



def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        OTP = get_random_string(length=6, allowed_chars='0123456789')
        request.session['otp'] = OTP
        send_mail(
            'Your OTP for registration',
            f'Your OTP is: {OTP}',
            settings.EMAIL_HOST,
            [email],
            fail_silently=False,
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        OTP = request.session['otp']
        print(otp, OTP)
        if OTP == otp:
            # del request.session['otp']
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})



def OrganizationRegistrationView(request):

    if request.method == 'POST':

        head_firstname = request.POST.get('head_firstname')
        head_lastname = request.POST.get('head_lastname')
        head_email = request.POST.get('head_email')
        head_phone_number = request.POST.get('head_phone_number')
        org_registration_number = request.POST.get('org_registration_number')
        org_email = request.POST.get('org_email')
        org_phone_number = request.POST.get('org_phone_number')
        org_name = request.POST.get('org_name')
        org_type = request.POST.get('org_type')
        org_address = request.POST.get('org_address')
        org_state = request.POST.get('org_state')
        org_pincode = request.POST.get('org_pincode')
        org_password = make_password(request.POST.get('org_password'))

        if OrganizationHeads.objects.filter(email = head_email).exists() :
            message = 'Manager Email already exist'
            
        if OrganizationHeads.objects.filter(phone_number = head_phone_number).exists():
            message = 'Manager phone number already exist'
            return render(request, 'OrganizationRegistration.html', {'message': 'Head email or phone number already exists'})

        
        if UnverifiedOrganizations.objects.filter(registration_number = org_registration_number).exists() or \
            UnverifiedOrganizations.objects.filter(email = org_email).exists() or \
            UnverifiedOrganizations.objects.filter(phone_number = org_phone_number).exists():
            
            return render(request, 'OrganizationRegistration.html', {'message': 'Organization registration number, email, or phone number already exists'})

        head = OrganizationHeads.objects.create(
            firstname=head_firstname,
            lastname=head_lastname,
            email=head_email,
            phone_number=head_phone_number
        )


        org = UnverifiedOrganizations.objects.create(
            registration_number=org_registration_number,
            email=org_email,
            phone_number=org_phone_number,
            name=org_name,
            Type=org_type,
            address=org_address,
            state=org_state,
            pincode=org_pincode,
            password=org_password,
            head_id=head
        )

        
    return render(request, 'OrganizationRegistration.html')

def OrganizationLoginView(request):

    message = ''
    if request.method == 'POST':

        registration_number = request.POST['registration_number']
        password = request.POST['password']

        org = VerifiedOrganizations.objects.filter(registration_number = registration_number)

        if org.exists():
            org = VerifiedOrganizations.objects.get(registration_number = registration_number)
            password_matches=check_password(password, org.password)

            if password_matches :

                request.session['Auth'] = True 
                request.session['user_type'] = 'Organization' 
                request.session['id'] = org.id
                head = org.head_id
                request.session['head_id'] = head.id

                # data = {'key': org.organization_id}
                # url = '/profile/?key={}'.format(data['key'])
                return redirect('Organization:profile')
            else:
                message='Wrong password.'
        else:
            message='Invalid registration number. Please try again'

    return render(request, 'OrganizationLogin.html',{'message':message})


def DonorRegistrationView(request):

    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = make_password(request.POST.get('password'))


        if Donors.objects.filter(email = email).exists() :
            message = 'Email already exist.'
            return render(request, 'DonorRegistration.html', {'message': 'email already exists'})

            
        if Donors.objects.filter(phone_number = phone_number).exists():
            message = 'phone number already exist'
            return render(request, 'DonorRegistration.html', {'message': 'phone number already exists'})

        
        donor = Donors.objects.create(
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone_number=phone_number,
            password = password
        )
    return render(request, 'DonorRegistration.html')

def DonorLoginView(request):
    message = ''

    if request.method == 'POST':

        email = request.POST['email']
        password=request.POST['password']

        donor = Donors.objects.filter(email = email)

        if donor.exists():
            donor = Donors.objects.get(email = email)
            password_matches=check_password(password, donor.password)

            if password_matches :

                request.session['Auth'] = True 
                request.session['user_type'] = 'Donor' 
                request.session['id'] = donor.id

                # data = {'key': org.organization_id}
                # url = '/profile/?key={}'.format(data['key'])
                return redirect('Donor:Donor-Profile')
            else:
                message='Wrong password.'
        else:
            message='Invalid email. Please try again'

    return render(request, 'DonorLogin.html',{'message':message})


def ManagerRegistrationView(request):
    message = ''
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = make_password(request.POST.get('password'))


        if Manager.objects.filter(email = email).exists() :
            message = 'Email already exist.'
            return render(request, 'ManagerRegistration.html', {'message': 'email already exists'})

            
        if Manager.objects.filter(phone_number = phone_number).exists():
            message = 'phone number already exist'
            return render(request, 'ManagerRegistration.html', {'message': 'phone number already exists'})

        
        manager = Manager.objects.create(
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone_number=phone_number,
            password = password
        )
    return render(request, 'ManagerRegistration.html')


def ManagerLoginView(request):
    message = ''

    if request.method == 'POST':

        email = request.POST['email']
        password=request.POST['password']

        manager = Manager.objects.filter(email = email)

        if manager.exists():
            manager = Manager.objects.get(email = email)
            password_matches=check_password(password, manager.password)

            if password_matches :

                request.session['Auth'] = True 
                request.session['user_type'] = 'Manager' 
                request.session['id'] = manager.id

                # data = {'key': org.organization_id}
                # url = '/profile/?key={}'.format(data['key'])
                return redirect('Manager:managerprofile')
            else:
                message='Wrong password.'
        else:
            message='Invalid email. Please try again'

    return render(request, 'ManagerLogin.html',{'message':message})


def LogoutView(request):

    if 'Auth' in request.session :
        request.session.clear()
    return redirect('LandingPage') 