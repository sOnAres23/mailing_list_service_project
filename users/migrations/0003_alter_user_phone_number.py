# Generated by Django 5.1.2 on 2024-12-08 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_options_user_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name="Номер телефона"),
        ),
    ]
