# Generated by Django 5.1.2 on 2024-10-30 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(
                default="profile_images/default.jpg", upload_to="profile_images"
            ),
        ),
    ]
