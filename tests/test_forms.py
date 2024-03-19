from django.test import TestCase
from core.forms import ProjectForm


class ProjectFormTest(TestCase):
    def test_valid_project_form(self):
        form_data = {"project_name": "Test Project"}
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_empty_project_form(self):
        form_data = {}
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["project_name"],
            ["This field is required."]
        )
