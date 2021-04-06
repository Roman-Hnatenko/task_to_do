import csv
from django.contrib import messages
import secrets
from datetime import datetime
from django.http import Http404
from typing import Any, Dict
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic import ListView, RedirectView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task, User, InviteKey
from .forms import ActiveDateForm, DoneActiveDateForm, UploadFileForm, KeyForm
from .tasks import save_tasks_from_csv


class UserTasksMixin:
    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class TabMixin:
    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            tab_name=self.tab_name,
            import_link=self.import_link,
            *args, **kwargs
        )


class OutputCsvFileMixin:
    # paginate_by = None

    def render_to_response(self, context):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=tasks.csv'
        writer = csv.writer(response)
        writer.writerow(['Title', 'Description', 'Create Date', 'Complete Date'])

        for task in context['object_list']:
            writer.writerow([
                task.title,
                task.description,
                task.date.isoformat(),
                task.done_date.isoformat() if task.done_date else '',
            ])
        return response


class TaskListView(LoginRequiredMixin, UserTasksMixin, TabMixin, ListView):
    login_url = 'accounts/login/'
    model = Task
    ordering = '-pk'
    template_name = 'list/task_list.html'
    paginate_by = 5
    tab_name = 'all'
    import_link = 'output_file'
    filter_params: Dict[str, Any] = dict()
    class_form = ActiveDateForm
    date_form = None


    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(date_form=self.date_form, file_form=UploadFileForm(), *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.filter_params:
            queryset = queryset.filter(**self.filter_params)
        return queryset

    def get(self, request, *args, **kwargs):
        self.date_form = self.class_form(request.GET)
        if self.date_form.is_valid():
            self.filter_params = dict(**self.date_form.validate_dates(), **self.filter_params)
        return super().get(request, *args, **kwargs)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description']
    success_url = reverse_lazy('task_view')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserTasksMixin, UpdateView):
    model = Task
    fields = ['title', 'description']
    success_url = reverse_lazy('task_view')


class TaskDeleteView(LoginRequiredMixin, UserTasksMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task_view')


class ActiveTaskView(TaskListView):
    import_link = 'output_file_active'
    tab_name = 'active'
    filter_params = dict(
        done_date__isnull=True
    )


class DoneTaskView(TaskListView):
    import_link = 'output_file_done'
    class_form = DoneActiveDateForm
    tab_name = 'done'
    filter_params = dict(
        done_date__isnull=False
    )


class DoneButtonTaskView(LoginRequiredMixin, UserTasksMixin, RedirectView):
    url = reverse_lazy('task_view')
    http_method_names = ['post']
    model = Task

    def post(self, request, *args, **kwargs):
        pk_value = request.POST.get('pk')
        self.model.objects.filter(pk=pk_value).update(done_date=datetime.now())
        return super().post(request, *args, **kwargs)


class UploadCsvFileView(LoginRequiredMixin, UserTasksMixin, FormView):
    template_name = 'list/file_form.html'
    form_class = UploadFileForm
    success_url = reverse_lazy('task_view')
    model = Task

    def form_valid(self, form):
        reader = form.cleaned_data['file']

        tasks_list = [(
            row['Title'],
            row['Description'] if row['Description']  else '',
            row['Create Date'] if row['Create Date'] else datetime.now(),
            row['Complete Date'] if row['Complete Date'] else None,
        ) for row in reader if row['Title']]

        save_tasks_from_csv.delay(tasks_list, self.request.user.id)

        return super().form_valid(form)


class AllOutputCsvFileView(OutputCsvFileMixin, TaskListView):
    pass


class DoneOutputCsvFileView(OutputCsvFileMixin, DoneTaskView):
    pass


class ActiveOutputCsvFileView(OutputCsvFileMixin, ActiveTaskView):
    pass


class FriendsListView(LoginRequiredMixin, ListView):
    login_url = 'accounts/login/'
    template_name = 'list/friends_list.html'

    def get_queryset(self):
        return self.request.user.friends.all()


class KeyCreationView(LoginRequiredMixin, RedirectView):
    login_url = 'accounts/login/'
    class_success_name = 'link_showing'
    http_method_names = ['post']
    model = InviteKey

    def post(self, request, *args, **kwargs):
        key = secrets.token_urlsafe(20)
        self.model.objects.create(invitor=request.user)

        self.url = reverse(self.class_success_name, kwargs={'key': key})
        return super().post(request, *args, **kwargs)


class LinkShowingView(LoginRequiredMixin, TemplateView):
    template_name = 'list/link_showing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        key = self.kwargs.get('key')
        invite_link = self.request.build_absolute_uri(
            reverse('invitor_info', kwargs={'key': key})
        )
        context['invite_link'] = invite_link
        return context


class InvitorInfoView(LoginRequiredMixin, DetailView):
    template_name = 'list/invitor_info.html'
    model = InviteKey
    slug_url_kwarg = 'key'
    slug_field = 'key'
    query_pk_and_slug = True
    context_object_name = 'key'

    def get_context_data(self, **kwargs):
        form = KeyForm(initial={'key': self.kwargs['key']})
        return super().get_context_data(form=form, **kwargs)

    def get_object(self, queryset=None):
        key_obj = super().get_object(queryset=queryset)
        if key_obj.is_active() and not self.request.user == key_obj.invitor:
            return key_obj
        raise Http404()


class InviteAcceptingView(LoginRequiredMixin, FormView):
    success_url = reverse_lazy('friends_list')
    form_class = KeyForm

    def form_valid(self, form):

        key_obj = InviteKey.objects.get(key=form.cleaned_data['key'])
        key_obj.friend = self.request.user
        key_obj.save()
        self.request.user.friends.add(key_obj.invitor)
        return super().form_valid(form)
