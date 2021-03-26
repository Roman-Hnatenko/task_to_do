from .models import User
from django_registration.forms import RegistrationForm
from django import forms
from datetime import datetime


class RegisterForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User


class DateInput(forms.DateInput):
    input_type = 'date'


class DateTimeForm(forms.Form):

    date__date = forms.DateField(widget=DateInput(attrs={
        'max': datetime.now().strftime("%Y-%m-%d"),
        'class': 'ml-2 '
    }), label='Date of creation')
    date__date.required = False

    done_date__date = forms.DateField(widget=DateInput(attrs={
        'max': datetime.now().strftime("%Y-%m-%d"),
        'class': 'ml-2'
    }), label='Date of complete')
    done_date__date.required = False
