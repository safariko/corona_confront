from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomSignupForm, InsuranceForm, ProfileForm, ReimburseForm, EmergencyProfileForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Customer, EmergencyProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
import stripe
from django.http import HttpResponse
from datetime import *
from dateutil.relativedelta import *


from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

from decouple import config




stripe.api_key = config("STRIPE_SECRET_KEY")

def home(request):
    return render(request, 'plans/home.html')


def join(request):
    return render(request, 'plans/join.html')

def get_started(request):
    return render(request, 'plans/get_started.html')

def privacy(request):
    return render(request, 'registration/privacy.html')

@login_required
def confirmation(request):
    if request.user.customer.membership:
        membership = True
    else:
        membership = False
    try:
        last_day_show = request.user.customer.last_day_membership
    except:
        last_day_show = None


    return render(request, 'registration/confirmation.html', {'last_day_show': last_day_show, 'membership': membership})

@login_required
def checkout(request):

    try:
        if request.user.customer.membership:
            return redirect('settings')
    except Customer.DoesNotExist:
        pass

    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = None

    if request.method == 'POST':
        stripe_customer = stripe.Customer.create(email=request.user.email, source=request.POST['stripeToken'])
        plan = 'plan_H3uyzsIvrQNhi7'
        if request.POST['plan'] == '3monthly':
            plan = 'plan_H3uzl32jJull1k'
        subscription = stripe.Subscription.create(customer=stripe_customer.id, items=[{'plan':plan}])

        customer.user = request.user
        customer.stripeid = stripe_customer.id
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = subscription.id
        customer.last_day_membership = datetime.now()+relativedelta(months=+1)
        if request.POST['plan'] == '3monthly':
            customer.last_day_membership = datetime.now()+relativedelta(months=+3)
        customer.save()

        return redirect('confirmation')
    else:
        plan = 'monthly'
        price = 900
        og_dollar = 9
        final_dollar = 9
        if request.method == 'GET' and 'plan' in request.GET:
            if request.GET['plan'] == '3monthly':
                plan = '3monthly'
                price = 2500
                og_dollar = 25
                final_dollar = 25

        return render(request, 'plans/checkout.html',
        {'plan':plan, 'price':price,'og_dollar':og_dollar,
        'final_dollar':final_dollar})





@user_passes_test(lambda u: u.is_superuser)
def updateaccounts(request):
    customers = Customer.objects.all()
    for customer in customers:
        subscription = stripe.Subscription.retrieve(customer.stripe_subscription_id)
        if subscription.status != 'active':
            customer.membership = False
        else:
            customer.membership = True
        customer.cancel_at_period_end = subscription.cancel_at_period_end
        customer.save()
    return HttpResponse('completed')

@login_required
def cancel_insurance(request):
    membership = False
    cancel_at_period_end = False
    last_day_show = None
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()
    else:
        try:
            if request.user.customer.membership:
                membership = True
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
            if request.user.customer.last_day_membership:
                last_day_show = request.user.customer.last_day_membership
        except Customer.DoesNotExist:
            membership = False


    return render(request, 'registration/cancel_insurance.html', {'membership':membership,
    'cancel_at_period_end':cancel_at_period_end, 'last_day_show': last_day_show })


@login_required(login_url='signup')
def new_insurance(request):
    try:
        if request.user.customer.membership:
            return redirect('settings')
    except Customer.DoesNotExist:
        pass

    try:
        profile = request.user.customer
    except Customer.DoesNotExist:
        profile = None

    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = InsuranceForm(instance=profile)
    else:
        # POST data submitted; process data.
        form = InsuranceForm(data=request.POST, instance=profile)
        if form.is_valid():
            new_profile = form.save()
            new_profile.refresh_from_db()
            new_profile.insurance_exists = form.cleaned_data.get('insurance_exists')
            new_profile.save()
            return redirect('new_profile')


    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/new_insurance.html', context)


@login_required
def new_profile(request):
    try:
        if request.user.customer.membership:
            return redirect('settings')
    except Customer.DoesNotExist:
        pass

    try:
        profile = request.user.customer
    except Customer.DoesNotExist:
        profile = None


    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ProfileForm(instance=profile)
    else:
        # POST data submitted; process data.
        form = ProfileForm(data=request.POST, instance=profile)
        if form.is_valid():
            new_profile = form.save()
            new_profile.refresh_from_db()
            new_profile.first_name = form.cleaned_data.get('first_name')
            new_profile.last_name = form.cleaned_data.get('last_name')
            new_profile.birth_date = form.cleaned_data.get('birth_date')
            new_profile.save()
            return redirect('join')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/new_profile.html', context)


@login_required
def reimburse(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ReimburseForm()
    else:
        # POST data submitted; process data.
        form = ReimburseForm(data=request.POST)
        if form.is_valid():
            reimburse = form.save(commit=False)
            reimburse.owner = request.user
            reimburse.save()
            return redirect('home')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/reimburse.html', context)






@login_required
def emergency_profile(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EmergencyProfileForm()
    else:
        # POST data submitted; process data.
        form = EmergencyProfileForm(data=request.POST)
        if form.is_valid():
            emergency_profile = form.save(commit=False)
            emergency_profile.owner = request.user
            emergency_profile.save()
            return redirect('settings')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/emergency_profile.html', context)



@login_required
def settings(request):

    membership = False
    cancel_at_period_end = False
    if request.method != 'POST':
        try:
            if request.user.customer.membership:
                membership = True
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False

    # """Show all topics."""

    try:
        profile = request.user.customer
    except Customer.DoesNotExist:
        profile = None



    try:
        emergency_profile = EmergencyProfile.objects.filter(owner=request.user).latest('date_added')
    except EmergencyProfile.DoesNotExist:
        emergency_profile = None

    try:
        last_day_show = request.user.customer.last_day_membership
    except:
        last_day_show = None



    context = {'profile': profile, 'membership': membership, 'cancel_at_period_end' : cancel_at_period_end,
               'emergency_profile': emergency_profile, 'last_day_show': last_day_show}
    return render(request, 'registration/settings.html', context)





def account_activation_sent(request):

    return render(request, 'registration/account_activation_sent.html')

def activate(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.customer.email_confirmed = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'registration/account_activation_invalid.html')



def register(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            current_site = get_current_site(request)
            subject = 'Activate Your CoronaConfront Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('new_insurance')
    else:
        form = CustomSignupForm()
    return render(request, 'registration/signup.html', {'form': form})



