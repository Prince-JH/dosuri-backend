# Generated by Django 4.1.2 on 2023-01-19 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0073_alter_hospital_last_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='status',
            field=models.CharField(default='active', max_length=32, null=True),
        ),
    ]
