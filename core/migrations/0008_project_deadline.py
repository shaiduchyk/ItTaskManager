from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_alter_task_assignees"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="deadline",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
