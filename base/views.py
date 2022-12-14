from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from .models import Task


class CustomLoginRequiredMixin(LoginRequiredMixin):
    redirect_field_name = settings.REDIRECT_FIELD_NAME


class TaskList(CustomLoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        search = self.request.GET.get('search') or ''

        if search:
            context['tasks'] = context['tasks'].filter(title__icontains=search)

        context['search'] = search

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()

        return (
            render(request, 'base/403.html')
            if task.user != self.request.user
            else super(TaskDetail, self).dispatch(request, *args, **kwargs)
        )


class TaskCreate(CustomLoginRequiredMixin, CreateView):
    model = Task
    template_name = 'base/task_create.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('base:tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(CustomLoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'base/task_update.html'
    fields = ['title', 'description', 'complete']

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(TaskUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('base:task', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()

        if task.user != self.request.user:
            return render(request, 'base/403.html')

        return super(TaskUpdate, self).dispatch(request, *args, **kwargs)


class TaskDelete(CustomLoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'base/task_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('base:tasks')

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()

        if task.user != self.request.user:
            return render(request, 'base/403.html')

        return super(TaskDelete, self).dispatch(request, *args, **kwargs)


class UserLogin(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True


class UserLogout(LogoutView):
    next_page = 'base:login'
    template_name = 'base/logout.html'


class UserRegistration(FormView):
    template_name = 'base/registration.html'
    form_class = UserCreationForm
    success_url = 'base:tasks'

    def form_valid(self, form):
        user = form.save()

        if user is not None:
            login(self.request, user)

        return super(UserRegistration, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('base:tasks')

        return super(UserRegistration, self).get(request, *args, **kwargs)


def page_not_find_view(request, exception):
    return render(request, 'base/404.html', status=404)
