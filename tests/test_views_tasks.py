from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from core.models import Task, TaskType, Project


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass", position=None,
        )
        self.task_type = TaskType.objects.create(type="Test Task Type")
        self.project = Project.objects.create(project_name="Test Project")

    def test_task_str_representation(self):
        task = Task.objects.create(
            task_name="Test Task",
            description="Task description",
            deadline=timezone.now(),
            is_completed=False,
            priority="Medium",
            task_type=self.task_type,
            project=self.project,
        )
        task.assignees.add(self.user)

        expected_str = (
            f"{task.task_name} assigned to   position: {self.user.position or "None"}"
            f" with {task.priority} priority"
        )
        self.assertEqual(str(task), expected_str)

    def test_task_with_assignees(self):
        task = Task.objects.create(
            task_name="Test Task",
            description="Task description",
            deadline=timezone.now(),
            is_completed=False,
            priority="Medium",
            task_type=self.task_type,
            project=self.project,
        )
        task.assignees.add(self.user)

        self.assertEqual(task.assignees.count(), 1)
        self.assertIn(self.user, task.assignees.all())

    def test_completed_task(self):
        task = Task.objects.create(
            task_name="Test Task",
            description="Task description",
            deadline=timezone.now(),
            is_completed=True,
            priority="Medium",
            task_type=self.task_type,
            project=self.project,
            done_at=timezone.now(),
        )

        self.assertTrue(task.is_completed)
        self.assertIsNotNone(task.done_at)
