from django import forms
from django.forms import DateInput
from .models import Task


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "task_name",
            "description",
            "task_type",
            "deadline",
            "priority",
            "assignees"
        ]

        widgets = {
            "deadline": DateInput(attrs={"type": "date"}),
            "assignees": forms.CheckboxSelectMultiple()
        }
