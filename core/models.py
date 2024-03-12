from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )

    class Meta:
        verbose_name_plural = "Workers"
        constraints = [
            UniqueConstraint(fields=["username"], name="unique_username")
        ]
        ordering = ["last_name", "first_name", "position",]

    def __str__(self):
        return f"{self.first_name} {self.last_name} position: {self.position}"

    def get_absolute_url(self):
        return reverse("core:worker-profile", kwargs={"pk": self.pk})


class TaskType(models.Model):
    type = models.CharField(max_length=63)

    def __str__(self):
        return self.type


class Project(models.Model):
    project_name = models.CharField(max_length=120)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    assignees = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name="project"
    )

    deadline = models.DateField(blank=True, null=True)
    done_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.project_name


class Task(models.Model):

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Urgent", "Urgent"),
        ("Critical", "Critical"),
    ]

    task_name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks",
        blank=True,
        null=True,
    )
    assignees = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name="tasks",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    done_at = models.DateTimeField(blank=True, null=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        default=None,
    )

    def __str__(self):
        assignee_names = ", ".join(
            str(assignee) for assignee in self.assignees.all()
        )
        return (f"{self.task_name} assigned to {assignee_names}"
                f" with {self.priority} priority")
