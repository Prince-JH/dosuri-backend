# Generated by Django 4.1.2 on 2022-12-07 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0021_remove_hospitaltreatment_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitaltreatment',
            name='description',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
