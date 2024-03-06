from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


import pretty_errors

from .models import Position, Worker, Task, TaskType, Project


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_tasks = Task.objects.count()
    last_added_task = Task.objects.order_by("-created_at").first()
    completed_tasks = Project.objects.filter(is_completed=True).count()
    context = {
        "num_tasks": num_tasks,
        "last_added_task": last_added_task,
        "completed_tasks": completed_tasks,
    }

    return render(request, "core/index.html", context)


class MyTasksListView(generic.ListView):
    model = Task
    template_name = 'core/my_tasks.html'
    context_object_name = 'task_list'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.incomplete_tasks_count = None
        self.completed_tasks_count = None

    def get_queryset(self):
        completed_tasks_count = Task.objects.filter(assignees=self.request.user, is_completed=True).count()
        incomplete_tasks_count = Task.objects.filter(assignees=self.request.user, is_completed=False).count()

        self.completed_tasks_count = completed_tasks_count
        self.incomplete_tasks_count = incomplete_tasks_count

        return Task.objects.filter(assignees=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["completed_tasks_count"] = self.completed_tasks_count
        context["incomplete_tasks_count"] = self.incomplete_tasks_count
        return context
