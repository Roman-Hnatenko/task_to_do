from copy import copy
from datetime import datetime
from django_registration.forms import RegistrationForm
from django import forms
from .models import User
from .fields import TaskCsvFileFied

class RegisterForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User


class DateInput(forms.DateInput):
    input_type = 'date'


class ActiveDateForm(forms.Form):

    date__date = forms.DateField(widget=DateInput(attrs={
        'max': datetime.now().strftime('%Y-%m-%d'),
        'class': 'ml-2 '
    }), label='Date of creation')
    date__date.required = False


    def validate_dates(self):
        cleaned_dates = super().clean()
        return {key: value for key, value in cleaned_dates.items() if value}


class DoneActiveDateForm(ActiveDateForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['done_date__date'] = copy(self.fields['date__date'])
        self.fields['done_date__date'].label = 'Date of complete'


class UploadFileForm(forms.Form):
    file = TaskCsvFileFied()


class KeyForm(forms.Form):
    key = forms.CharField(widget=forms.HiddenInput)
