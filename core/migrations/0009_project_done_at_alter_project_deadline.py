from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_project_deadline"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="done_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="deadline",
            field=models.DateField(blank=True, null=True),
        ),
    ]
