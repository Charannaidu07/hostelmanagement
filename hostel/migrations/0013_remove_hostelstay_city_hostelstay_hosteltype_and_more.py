# Generated by Django 5.1.3 on 2025-03-15 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hostel", "0012_hostelstay_priority1_hostelstay_priority2_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="hostelstay",
            name="city",
        ),
        migrations.AddField(
            model_name="hostelstay",
            name="hosteltype",
            field=models.CharField(
                choices=[("choose", "Choose"), ("ac", "AC"), ("nonac", "Non AC")],
                default="Choose",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="hostelstay",
            name="location",
            field=models.CharField(
                choices=[
                    ("choose", "Choose"),
                    ("Hyderabad", "hyderabad"),
                    ("Chennai", "Chennai"),
                ],
                default="Choose",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="hostelstay",
            name="share",
            field=models.IntegerField(
                choices=[("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6)], default="5"
            ),
        ),
    ]
