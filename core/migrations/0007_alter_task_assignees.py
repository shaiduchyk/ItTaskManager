from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_task_done_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="assignees",
            field=models.ManyToManyField(
                blank=True, related_name="tasks", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
