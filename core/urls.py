from django.urls import path

from core.views import (
    index,
    MyTasksListView,
    AllTasksListView,
    OurTeamsListView,
    create_task,
    take_task,
    mark_as_done,
    TaskDeleteView,
)

app_name = "core"

urlpatterns = [
    path("", index, name="index"),
    path("my-tasks/",
         MyTasksListView.as_view(),
         name="my-tasks"),
    path("all-tasks/",
         AllTasksListView.as_view(),
         name="all-tasks"),
    path("our-teams/",
         OurTeamsListView.as_view(),
         name="our-teams"),
    path("create_task/",
         create_task,
         name="create-task"),
    path("take-task/<int:task_id>/",
         take_task, name="take-task"),
    path("mark-as-done/<int:task_id>/",
         mark_as_done,
         name="mark-as-done"),
    path("task-delete/<int:pk>/delete/",
         TaskDeleteView.as_view(),
         name="task-delete"),
]
