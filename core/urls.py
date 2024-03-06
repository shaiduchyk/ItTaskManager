from django.urls import path

from core.views import (
    index,
    MyTasksListView,
    AllTasksListView,
    OurTeamsListView,
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
         name="our-teams")
]
