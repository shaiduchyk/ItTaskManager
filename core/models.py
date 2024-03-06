from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class Position(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Position"


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)


class TaskType(models.Model):
    type = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.type


class Task(models.Model):
    PRIORITY_LOW = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_HIGH = 3
    PRIORITY_URGENT = 4
    PRIORITY_CRITICAL = 5

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
        (PRIORITY_URGENT, "Urgent"),
        (PRIORITY_CRITICAL, "Critical"),
    ]

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES, default="Low")
    task_type = models.ForeignKey("TaskType", on_delete=models.CASCADE)
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="task")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} assigned to {self.assignees} with {self.priority} priority"
