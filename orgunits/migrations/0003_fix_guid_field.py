# Generated by Django 3.1.7 on 2021-03-13 10:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("orgunits", "0002_fix_guid_field"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organization",
            name="code",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, unique=True, verbose_name="код"
            ),
        ),
    ]
