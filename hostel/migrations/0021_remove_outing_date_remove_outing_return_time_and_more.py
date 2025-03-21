# Generated by Django 5.1.3 on 2025-03-15 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hostel", "0020_outing_approved_alter_outing_reason"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="outing",
            name="date",
        ),
        migrations.RemoveField(
            model_name="outing",
            name="return_time",
        ),
        migrations.AddField(
            model_name="outing",
            name="indate",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="outing",
            name="intime",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="outing",
            name="outdate",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="outing",
            name="outtime",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="outing",
            name="outtype",
            field=models.CharField(
                choices=[
                    ("day", "Day Outing"),
                    ("home", "Home Outing"),
                    ("emergency", "Emergency"),
                ],
                default="day",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="outing",
            name="reason",
            field=models.TextField(blank=True, null=True),
        ),
    ]
