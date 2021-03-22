from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task


class UserTasksMixin:

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class TaskListView(LoginRequiredMixin, UserTasksMixin, ListView):
    login_url = 'accounts/login/'
    model = Task
    template_name = 'list/index.html'
    ordering = '-pk'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['task_text']
    success_url = reverse_lazy('task-view')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserTasksMixin, UpdateView):
    model = Task
    fields = ['task_text']
    success_url = reverse_lazy('task-view')


class TaskDeleteView(LoginRequiredMixin, UserTasksMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task-view')





