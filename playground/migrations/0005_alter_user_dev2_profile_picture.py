# Generated by Django 4.2.2 on 2023-10-17 22:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("playground", "0004_user_dev2_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user_dev2",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="profile_pictures",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        ["png", "jpg", "jpeg"]
                    )
                ],
            ),
        ),
    ]
