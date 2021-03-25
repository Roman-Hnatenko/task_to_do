from .models import User, Task
from django_registration.forms import RegistrationForm
from django import forms


class RegisterForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User


class DateForm(forms.Form):
    date = forms.DateField()

