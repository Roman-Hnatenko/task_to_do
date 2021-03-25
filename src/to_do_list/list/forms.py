from .models import User, Task
from django_registration.forms import RegistrationForm
from django import forms
from datetime import datetime


class RegisterForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User


class DateInput(forms.DateInput):
    input_type = 'date'


class DateForm(forms.Form):
    date = forms.DateField(widget=DateInput(attrs={
        'max': datetime.now().strftime("%Y-%m-%d"),
        'class': 'ml-2'
    }), label='Date of creation')
