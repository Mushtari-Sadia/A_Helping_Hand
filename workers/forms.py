from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from customers import forms as customer_forms


JOB_LIST = [
    ('1','Electrician'),
    ('2','Home Cleaner'),
    ('3','Pest Control Service'),
    ('4','Plumber'),
    ('5','Nurse'),
    ('6','House Shifting Assistant'),
    ('7','Carpenter')

]


class WorkerRegisterForm(customer_forms.CustomerRegisterForm):
    email = forms.EmailField()
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
                                 max_length=32)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
                                max_length=32)
    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=customer_forms.BIRTH_YEAR_CHOICES))
    birth_year.label = "Date of birth"
    first_name.label = "Full Name"
    last_name.label = ""
    area_field = forms.ChoiceField(
        widget=forms.Select,
        choices=customer_forms.AREA_LIST,
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
        fields = ['username','first_name','last_name','email', 'password1', 'password2','birth_year','area_field','address','job_field']

