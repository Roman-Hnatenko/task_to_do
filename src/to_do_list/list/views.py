from datetime import datetime
from typing import Any, Dict
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import DateForm


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
    date_form = None

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            date_form=self.date_form,
            *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.filter_params:
            queryset = queryset.filter(**self.filter_params)
        return queryset

    def get(self, request, *args, **kwargs):
        self.date_form = DateForm(request.GET)

        if self.date_form.is_valid():
            self.filter_params = dict(**self.date_form.cleaned_data, **self.filter_params)
        return super().get(request, *args, **kwargs)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description']
    success_url = reverse_lazy('task-view')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserTasksMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'done']
    success_url = reverse_lazy('task-view')

    def post(self, request, *args, **kwargs):
        if request.POST.get('done'):
            self.model.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg)).update(done_date=datetime.now())
        return super().post(request, *args, **kwargs)


class TaskDeleteView(LoginRequiredMixin, UserTasksMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task-view')


class ActiveTaskView(TaskListView):
    tab_name = 'active'
    filter_params = dict(
        done=False
    )


class DoneTaskView(TaskListView):
    tab_name = 'done'
    filter_params = dict(
        done=True
    )
