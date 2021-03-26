from .models import User
from django_registration.forms import RegistrationForm
from django import forms
from datetime import datetime


class RegisterForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User


class DateInput(forms.DateInput):
    input_type = 'date'


class DateForm(forms.Form):
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

    def clean(self):
        cleaned_date = super().clean()
        cleaned_date = {key: value for key, value in cleaned_date.items() if value}
        return cleaned_date
