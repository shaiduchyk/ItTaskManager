from django import forms
from django.forms import DateInput
from .models import Task, Project


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "task_name",
            "description",
            "task_type",
            "deadline",
            "priority",
            "assignees",
            "project",
        ]

        widgets = {
            "deadline": DateInput(attrs={"type": "date"}),
            "assignees": forms.CheckboxSelectMultiple(),
            "done_at": DateInput(attrs={'type': 'date'})
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "project_name",
            "description",
            "assignees",
            "deadline",
            "done_at"
        ]

        widgets = {
            "deadline": DateInput(attrs={'type': 'date'}),
            "assignees": forms.CheckboxSelectMultiple(),
            "done_at": DateInput(attrs={'type': 'date'})
        }
