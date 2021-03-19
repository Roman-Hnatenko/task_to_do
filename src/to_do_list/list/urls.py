from django.urls import include, path
from django_registration.backends.one_step.views import RegistrationView
from django.contrib.auth.views import LogoutView
from . import views


from .forms import RegisterForm

urlpatterns = [
    path('', views.ViewListTask.as_view()),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', RegistrationView.as_view(form_class=RegisterForm), name='django_registration_register',),
    path('accounts/logout/', LogoutView.as_view(template_name="registration/logout.html"), name='logout'),
    path('accounts/', include('django_registration.backends.one_step.urls'))
]
