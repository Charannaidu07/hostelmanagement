# Generated by Django 5.1.3 on 2025-03-15 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hostel", "0017_hostelstay_priority1_hostelstay_priority2_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hostelstay",
            name="profile_picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="profile_pictures/"
            ),
        ),
    ]
