from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_alter_worker_position"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.CharField(
                choices=[
                    (1, "Low"),
                    (2, "Medium"),
                    (3, "High"),
                    (4, "Urgent"),
                    (5, "Critical"),
                ],
                max_length=10,
            ),
        ),
    ]
