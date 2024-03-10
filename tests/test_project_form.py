from django.test import TestCase
from django.urls import reverse


class ProjectFormTest(TestCase):
    def test_valid_project_form_submission(self):
        form_data = {"project_name": "Test Project"}
        response = self.client.post(
            reverse("core:project-create"), data=form_data
        )
        self.assertEqual(response.status_code, 302)
