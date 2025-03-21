# Generated by Django 5.1.3 on 2025-03-14 03:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hostel", "0002_hostelstay"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="hostelstay",
            name="city",
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="hostelstay",
            name="gender",
            field=models.CharField(
                choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
                default="Male",
                max_length=10,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="hostelstay",
            name="guardian_mobile",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name="hostelstay",
            name="house_address",
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="hostelstay",
            name="location",
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="hostelstay",
            name="parent_mobile",
            field=models.CharField(default=None, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="hostelstay",
            name="payment_due",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="hostelstay",
            name="share_type",
            field=models.CharField(
                choices=[
                    ("Single", "Single"),
                    ("Double", "Double"),
                    ("Triple", "Triple"),
                ],
                default=None,
                max_length=50,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="hostelstay",
            name="user_mobile",
            field=models.CharField(default=None, max_length=15),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="PaymentHistory",
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
                ("amount_paid", models.IntegerField()),
                ("payment_date", models.DateField(auto_now_add=True)),
                ("payment_proof", models.ImageField(upload_to="payments/")),
                ("verified", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
