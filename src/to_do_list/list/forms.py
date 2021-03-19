from .models import User

from django_registration.forms import RegistrationForm


class RegisterForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User

