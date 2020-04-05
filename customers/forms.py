from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import datetime

now = datetime.datetime.now()
BIRTH_YEAR_CHOICES = []
inYr = now.year-80
while inYr!=now.year-15 :
    BIRTH_YEAR_CHOICES.append(str(inYr))
    inYr += 1



AREA_LIST_ALL = [
'Adabar',
'Azampur',
'Badda',
'Bangsal',
'Bimanbandar',
'Cantonment ',
'Chowkbazar ',
'Darus Salam ',
'Demra ',
'Dhanmondi',
'Gendaria',
'Gulshan',
'Hazaribagh',
'Kadamtali',
'Kafrul',
'Kalabagan',
'Kamrangirchar',
'Khilgaon',
'Khilkhet',
'Kotwali',
'Lalbagh',
'Mirpur Model',
'Mohammadpur',
'Motijheel',
'New Market',
'Pallabi',
'Paltan',
'Panthapath',
'Ramna',
'Rampura',
'Sabujbagh',
'Shah Ali',
'Shahbag',
'Sher-e-Bangla Nagar',
'Shyampur',
'Sutrapur',
'Tejgaon Industrial Area',
'Tejgaon',
'Turag',
'Uttar Khan',
'Uttara ',
'Vatara',
'Wari']

AREA_LIST = []

x=1
for i in AREA_LIST_ALL:
    AREA_LIST.append((str(x),i))
    x += 1


class CustomerRegisterForm(UserCreationForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
                                 max_length=11)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
                                 max_length=32)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
                                max_length=32)
    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    birth_year.label = "Date of birth"
    first_name.label = "Full Name"
    last_name.label = ""
    area_field = forms.ChoiceField(
        widget=forms.Select,
        choices=AREA_LIST,
    )
    area_field.label = "Address"
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House No.,Road No.,Sector/Block etc...'}),
                                 max_length=45,required=False)
    address.label = ""
    phone_number.label="Phone Number"

    class Meta:
         model = User
         fields = ['phone_number','first_name','last_name','email', 'password1', 'password2','birth_year','area_field','address']
