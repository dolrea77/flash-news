# Generated by Django 4.2.3 on 2023-11-15 00:02

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Crawring",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("content", models.TextField()),
                ("img", models.CharField(max_length=100)),
                ("src", models.CharField(default="default_value", max_length=100)),
                (
                    "summarize",
                    models.CharField(default="default_value", max_length=100),
                ),
            ],
        ),
    ]