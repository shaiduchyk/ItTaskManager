from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class Position(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)


class TaskType(models.Model):
    type = models.CharField(max_length=255, unique=True)


class Task(models.Model):

    PRIORITY_CHOICES = [
        ("Low",),
        ("Medium",),
        ("High",),
        ("Urgent",),
        ("Critical",),
    ]
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES, default="Low")
    task_type = models.ForeignKey("TaskType", on_delete=models.CASCADE)
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="task")
    created_at = models.DateTimeField(auto_now_add=True)
