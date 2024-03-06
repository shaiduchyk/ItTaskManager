from django import forms
from .models import Task


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "task_name",
            "description",
            "deadline",
            "priority",
            "assignees"
        ]
