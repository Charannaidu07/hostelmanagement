# Generated by Django 5.1.3 on 2025-03-14 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hostel", "0009_chatmessage_admin_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatmessage",
            name="admin_message",
            field=models.TextField(default=None),
        ),
    ]
