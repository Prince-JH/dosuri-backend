# Generated by Django 4.1.1 on 2022-10-03 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0002_user_date_joined_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateTimeField(blank=True),
        ),
    ]
