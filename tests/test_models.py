from django.test import TestCase
from core.models import Project


class ProjectModelTest(TestCase):
    def test_project_creation(self):
        project = Project.objects.create(project_name="Test Project")
        self.assertEqual(project.project_name, "Test Project")
