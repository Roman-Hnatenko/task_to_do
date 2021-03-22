from django.urls import include, path
from django_registration.backends.one_step.views import RegistrationView
from . import views


from .forms import RegisterForm

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-view'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', RegistrationView.as_view(form_class=RegisterForm), name='django_registration_register',),
    path('accounts/', include('django_registration.backends.activation.urls')),

    path('task/add/', views.TaskCreateView.as_view(), name='task-add'),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
]
