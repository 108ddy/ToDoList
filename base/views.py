from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Task


class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'


class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'


class TaskCreate(CreateView):
    model = Task
    template_name = 'base/task_create.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('base:tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(UpdateView):
    model = Task
    template_name = 'base/task_update.html'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('base:task')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(TaskUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('base:task', kwargs={'pk': self.object.pk})


class TaskDelete(DeleteView):
    model = Task
    template_name = 'base/task_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('base:tasks')
