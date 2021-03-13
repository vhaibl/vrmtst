# Generated by Django 3.1.7 on 2021-03-13 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("employees", "0002_fix_guid_field"),
        ("orgunits", "0003_fix_guid_field"),
    ]

    operations = [
        migrations.CreateModel(
            name="Shift",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start", models.DateTimeField(verbose_name="Начало")),
                ("end", models.DateTimeField(verbose_name="Окончание")),
                (
                    "employee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="employees.employee",
                        verbose_name="Сотрудник",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="orgunits.organization",
                        verbose_name="Организация",
                    ),
                ),
            ],
            options={"verbose_name": "Смена", "verbose_name_plural": "Смены",},
        ),
    ]