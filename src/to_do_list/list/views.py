import csv
from datetime import datetime
from typing import Any, Dict
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.list import BaseListView
from django.views.generic import ListView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import ActiveDateForm, DoneActiveDateForm, UploadFileForm


class UserTasksMixin:
    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class TabMixin:
    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            tab_name=self.tab_name,
            *args, **kwargs)


class TaskListView(LoginRequiredMixin, UserTasksMixin, TabMixin, ListView):
    login_url = 'accounts/login/'
    model = Task
    ordering = '-pk'
    template_name = 'list/task_list.html'
    paginate_by = 5
    tab_name = 'all'
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
    tab_name = 'active'
    filter_params = dict(
        done_date__isnull=True
    )


class DoneTaskView(TaskListView):
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


class OutputCsvView(LoginRequiredMixin, UserTasksMixin, BaseListView):
    model = Task

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


class UploadCsvView(LoginRequiredMixin, UserTasksMixin, FormView):
    template_name = 'list/file_form.html'
    form_class = UploadFileForm
    success_url = reverse_lazy('task_view')
    model = Task

    def form_valid(self, form):

        reader = form.cleaned_data['file']
        print(reader)
        for row in reader:
            self.model.objects.create(
                title=row['Title'],
                description=row['Description'],
                date=row['Create Date'],
                done_date = datetime.fromisoformat(row['Complete Date']) if row['Complete Date'] else None,
                author=self.request.user
            )

        return super().form_valid(form)
