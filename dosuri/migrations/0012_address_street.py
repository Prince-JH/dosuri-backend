# Generated by Django 4.1.2 on 2022-11-04 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0011_hospitaltreatment_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='street',
            field=models.CharField(max_length=64, null=True),
        ),
    ]