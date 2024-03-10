from django.contrib.auth.decorators import login_required
from django.db.models import Value, QuerySet, Count
from django.db.models.functions import Coalesce
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Worker, Task, Project
from .forms import TaskCreationForm, ProjectForm, ProjectSearchForm


@login_required
def index(request: HttpRequest) -> HttpResponse:
    user = request.user

    all_tasks = Task.objects.filter(assignees=user)
    completed_tasks = all_tasks.filter(is_completed=True)
    incompleted_tasks = all_tasks.filter(is_completed=False)

    context = {
        "all_tasks": all_tasks.count(),
        "completed_tasks_count": completed_tasks.count(),
        "incompleted_tasks_count": incompleted_tasks.count(),
    }

    return render(request, "core/index.html", context)


class MyTasksListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "my_tasks.html"
    context_object_name = "task_list"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.incomplete_tasks_count = None
        self.completed_tasks_count = None

    def get_queryset(self):
        tasks = Task.objects.filter(assignees=self.request.user)

        tasks_counts = tasks.values("is_completed").annotate(count=Count("id"))

        for count_info in tasks_counts:
            if count_info["is_completed"]:
                self.completed_tasks_count = count_info["count"]
            self.incomplete_tasks_count = count_info["count"]

        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["completed_tasks_count"] = self.completed_tasks_count
        context["incomplete_tasks_count"] = self.incomplete_tasks_count
        return context


class AllTasksListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "all_tasks.html"
    paginate_by = 8
    context_object_name = "task_list"
    all_possible_tasks = Task.objects.count()

    def get_queryset(self) -> QuerySet:
        return Task.objects.annotate(
            responsible=Coalesce("assignees__username", Value("Not assigned"))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OurTeamsListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "our_teams.html"
    paginate_by = 8
    context_object_name = "team_members"

    def get_queryset(self) -> QuerySet:
        return Worker.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def create_task(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()
            return redirect("core:all-tasks")
    else:
        form = TaskCreationForm()

    return render(
        request,
        "core/create_task.html",
        {"form": form, "user_position": request.user.position},
    )


@login_required
def take_task(request: HttpRequest, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, id=task_id)
    task.assignees.add(request.user)
    return redirect("core:all-tasks")


@login_required
def mark_as_done(request: HttpRequest, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, id=task_id)
    task.is_completed = True
    task.done_at = timezone.now()
    task.save()
    return HttpResponseRedirect(
        request.META.get(
            "HTTP_REFERER",
            reverse_lazy(viewname="core:my-tasks"))
    )


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("core:all-tasks")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("core:all-tasks")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    fields = ["position", "first_name", "last_name", "password"]
    success_url = reverse_lazy("core:our-teams")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ["position", "first_name", "last_name", "username"]
    success_url = reverse_lazy("core:our-teams")


class WorkerProfileView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "worker_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        completed_tasks = Task.objects.filter(
            assignees=self.object, is_completed=True
        )
        incomplete_tasks = Task.objects.filter(
            assignees=self.object, is_completed=False
        )

        context["completed_tasks"] = completed_tasks
        context["incomplete_tasks"] = incomplete_tasks

        return context


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    fields = "__all__"
    paginate_by = 7

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context["search_form"] = ProjectSearchForm
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ProjectSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                project_name__icontains=form.cleaned_data["project_name"]
            )
        return queryset


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("core:project-list")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "project_form.html"
    success_url = reverse_lazy("core:project-list")


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "create_project.html"
    success_url = reverse_lazy("core:project-list")


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
