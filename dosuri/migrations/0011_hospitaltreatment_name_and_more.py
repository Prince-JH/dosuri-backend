# Generated by Django 4.1.2 on 2022-11-01 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0010_alter_hospitaltreatment_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitaltreatment',
            name='name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='hospitaltreatment',
            name='description',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
