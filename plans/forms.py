from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Customer, EmergencyProfile, Reimburse

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')





class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['insurance_exists']
        labels = {'insurance_exists': ''}



class ProfileForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'birth_date']
        labels = {'first_name': 'First Name ', 'last_name': 'Last Name ', 'birth_date': 'Date of Birth '}



class EmergencyProfileForm(forms.ModelForm):

    class Meta:
        model = EmergencyProfile
        fields = ['emergency_first_name', 'emergency_last_name', 'emergency_email']
        labels = {'emergency_first_name': 'First Name ', 'emergency_last_name': 'Last Name ', 'emergency_email': 'Email '}



class ReimburseForm(forms.ModelForm):

    class Meta:
        model = Reimburse
        fields = ['hosp_date', 'hosp_name', 'hosp_location', 'deductible_amount', 'address_one', 'address_two', 'city', 'state', 'zip_code' ]
        # fields = ['hosp_date', 'hosp_location', 'deductible_amount' ]
        labels = {'hosp_date': 'Hospitalization Date ', 'hosp_name': 'Hospital Name ', 'hosp_location': 'Hospital Location', 'deductible_amount': 'Deductible Amount ($)', 'address_one': 'Home Address', 'address_two': 'Apt No', 'city':'Home City', 'state':'Home State', 'zip_code':'Home Zip Code'}
            # labels = {'hosp_date': 'Cremation Date ', 'hosp_location': 'Cremation Location', 'deductible_amount': 'Cremation Cost'}

