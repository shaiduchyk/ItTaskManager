from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_alter_task_task_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="done_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
