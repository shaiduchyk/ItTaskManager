from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Value
from django.db.models.functions import Coalesce
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


import pretty_errors
from django.views.decorators.http import require_POST

from .models import Position, Worker, Task, TaskType, Project
from .forms import TaskCreationForm


@login_required
def index(request):
    user = request.user

    all_tasks = Task.objects.filter(assignees=user)

    completed_tasks = all_tasks.filter(is_completed=True)
    incompleted_tasks = all_tasks.filter(is_completed=False)

    context = {
        "all_tasks": all_tasks.count(),
        'completed_tasks_count': completed_tasks.count(),
        'incompleted_tasks_count': incompleted_tasks.count(),
    }

    return render(request, 'core/index.html', context)


class MyTasksListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "core/my_tasks.html"
    context_object_name = "task_list"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.incomplete_tasks_count = None
        self.completed_tasks_count = None

    def get_queryset(self):
        completed_tasks_count = Task.objects.filter(
            assignees=self.request.user, is_completed=True
        ).count()
        incomplete_tasks_count = Task.objects.filter(
            assignees=self.request.user, is_completed=False
        ).count()

        self.completed_tasks_count = completed_tasks_count
        self.incomplete_tasks_count = incomplete_tasks_count

        return Task.objects.filter(assignees=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["completed_tasks_count"] = self.completed_tasks_count
        context["incomplete_tasks_count"] = self.incomplete_tasks_count
        return context


class AllTasksListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "all_tasks.html"
    paginate_by = 5
    context_object_name = "task_list"

    def get_queryset(self):
        return Task.objects.annotate(
            responsible=Coalesce("assignees__username", Value("Not assigned"))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OurTeamsListView(generic.ListView):
    model = Worker
    template_name = "our_teams.html"
    paginate_by = 5
    context_object_name = "team_members"

    def get_queryset(self):
        return Worker.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('core:all-tasks')
    else:
        form = TaskCreationForm()

    return render(request, 'core/create_task.html', {'form': form, 'user_position': request.user.position})


@login_required
def take_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.assignees.add(request.user)
    return redirect('core:all-tasks')


@login_required
def mark_as_done(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_completed = True
    task.done_at = timezone.now()
    task.save()
    return redirect('core:all-tasks')
