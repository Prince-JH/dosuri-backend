# Generated by Django 4.1.2 on 2022-12-27 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0051_create_default_insurance'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
    ]
