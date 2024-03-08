from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_task_priority"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.CharField(
                choices=[
                    ("Low", "Low"),
                    ("Medium", "Medium"),
                    ("High", "High"),
                    ("Urgent", "Urgent"),
                    ("Critical", "Critical"),
                ],
                max_length=10,
            ),
        ),
    ]
