from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import datetime

# minimum user age = 15, max user age = 90
min_user_age = 15
max_user_age = 70

now = datetime.datetime.now()
BIRTH_YEAR_CHOICES = []
inYr = now.year-max_user_age
while inYr!=now.year-min_user_age :
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
         fields = ['phone_number','first_name','last_name', 'password1', 'password2','birth_year','area_field','address']


JOB_LIST = [
    ('1','Electrician'),
    ('2','Home Cleaner'),
    ('3','Pest Control Service'),
    ('4','Plumber'),
    ('5','Nurse'),
    ('6','House Shifting Assistant'),
    ('7','Carpenter')

]

OPTIONS = (
        (1, "AC"),
        (2, "TV"),
        (3, "FRIDGE"),
        (4, "GENERAL"),
    )


class WorkerRegisterForm(CustomerRegisterForm):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        max_length=11)
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
                                 max_length=45)
    address.label = ""
    job_field = forms.ChoiceField(
        widget=forms.Select,
        choices=JOB_LIST,
    )
    job_field.label = "What kind of work do you do?"



    class Meta:
        model = User
        fields = ['phone_number','first_name','last_name', 'password1', 'password2','birth_year','area_field','address','job_field']


class LoginForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        max_length=11)
    phone_number.label = "Phone Number"
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    password.label = "Password"


class ElectricianRegistrationForm(forms.Form):

    expertise = forms.MultipleChoiceField(initial=(4, "GENERAL"),widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)
    expertise.label = "What kind of Mechanic are you?"
    license_info = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your license information'}),
        max_length=20,required=False)
    license_info.label = "License Information (Optional)"

    yr_of_experience = forms.IntegerField(
        initial="0",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
        max_value=60,required=False
    )
    yr_of_experience.label = "Years of Experience (Optional)"

    qualification = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Educational qualifications'}),
        max_length=50,required=False)
    qualification.label = "Educational Qualification (Optional)"



class HomeCleanerRegistrationForm(forms.Form):
    NID_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your National Id No.'}),
        max_length=42)
    NID_number.label = "NID No."

class PestControlServiceRegistrationForm(forms.Form):
    license_info = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your license information'}),
        max_length=20, required=False)
    license_info.label = "License Information (Optional)"

    chemical_info = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'e.g : Acephate, Imidacloprid, Dinotefuran... '}),
        max_length=50, required=False)
    chemical_info.label = "Which insecticides and pesticides do you use? (Optional)"


class PlumberRegistrationForm(forms.Form):

    yr_of_experience = forms.IntegerField(initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
        max_value=60, required=False
    )
    yr_of_experience.label = "Years of Experience (Optional)"



class NurseRegistrationForm(forms.Form):

    certificate_info = forms.CharField(
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Enter your certificate information'}),
                                   max_length=20, required=False)
    certificate_info.label = "License Information (Optional)"

    qualification = forms.CharField(
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Describe your qualification'}),
                                   max_length=50, required=False)
    qualification.label = "Educational Qualification (Optional)"

    yr_of_experience = forms.IntegerField(initial=0,
                                          widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
                                          max_value=60, required=False
                                          )
    yr_of_experience.label = "Years of Experience (Optional)"



class HouseShiftingAssistantRegistrationForm(forms.Form):


    driving_license = forms.CharField(
                                       widget=forms.TextInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Enter your driving license'}),
                                       max_length=20, required=False)
    driving_license.label = "Driving License"

    car_type = forms.CharField(
                                      widget=forms.TextInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'What type of car?'}),
                                      max_length=20, required=False)
    car_type.label = "Type of Car"

    car_no = forms.CharField(
                                      widget=forms.TextInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'Enter your car no.'}),
                                      max_length=20, required=False)
    car_no.label = "Car No."


class CarpenterRegistrationForm(forms.Form):
    shop_name = forms.CharField(
                                      widget=forms.TextInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'Enter your shop name'}),
                                      max_length=20, required=False)
    shop_name.label = "Shop Name"

    shop_address = forms.CharField(
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Enter the address of your shop'}),
                               max_length=70, required=False)
    shop_address.label = "Shop Address"


