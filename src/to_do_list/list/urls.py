from django.urls import include, path
from django_registration.backends.one_step.views import RegistrationView
from . import views
from .forms import RegisterForm


urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_view'),
    path('done/task/', views.DoneButtonTaskView.as_view(), name='task_done_button'),
    path('active/', views.ActiveTaskView.as_view(), name='task_active'),
    path('done/', views.DoneTaskView.as_view(), name='task_done'),

    path('get_file/', views.AllOutputCsvFileView.as_view(), name='output_file'),
    path('get_file_done/', views.DoneOutputCsvFileView.as_view(), name='output_file_done'),
    path('get_file_active/', views.ActiveOutputCsvFileView.as_view(), name='output_file_active'),

    path('load-file/', views.UploadCsvFileView.as_view(), name='upload_file'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', RegistrationView.as_view(form_class=RegisterForm), name='django_registration_register',),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('task/add/', views.TaskCreateView.as_view(), name='task_add'),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),

    path('friends/', views.FriendsListView.as_view(), name='friends_list'),
    path('friends/create_key/', views.KeyCreationView.as_view(), name='creation_key'),
    path('friends/link_showing/<slug:key>/', views.LinkShowingView.as_view(), name='link_showing'),
    path('invitor_info/<slug:key>/', views.InvitorInfoView.as_view(), name='invitor_info'),
    path('accept/', views.InviteAcceptingView.as_view(), name='accept_invite'),

]
