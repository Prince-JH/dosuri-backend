# Generated by Django 4.1.2 on 2022-12-07 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0020_hospitaltreatmentassoc_article_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospitaltreatment',
            name='duration',
        ),
        migrations.AddField(
            model_name='hospitaltreatment',
            name='price_per_hour',
            field=models.IntegerField(null=True),
        ),
    ]