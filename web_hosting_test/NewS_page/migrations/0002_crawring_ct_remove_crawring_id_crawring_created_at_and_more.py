# Generated by Django 4.2.3 on 2023-11-21 23:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("NewS_page", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Crawring_ct",
            fields=[
                (
                    "title_ct",
                    models.CharField(
                        max_length=100, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("content_ct", models.TextField()),
                ("img_ct", models.CharField(max_length=100)),
                ("src_ct", models.CharField(max_length=100)),
                ("category", models.CharField(max_length=15)),
                ("summarize_ct", models.TextField()),
                ("created_at_ct", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="crawring",
            name="id",
        ),
        migrations.AddField(
            model_name="crawring",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="crawring",
            name="src",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="crawring",
            name="summarize",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="crawring",
            name="title",
            field=models.CharField(
                max_length=100, primary_key=True, serialize=False, unique=True
            ),
        ),
    ]