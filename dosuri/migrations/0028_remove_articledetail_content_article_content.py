# Generated by Django 4.1.2 on 2022-12-10 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0027_hospitalimage_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articledetail',
            name='content',
        ),
        migrations.AddField(
            model_name='article',
            name='content',
            field=models.CharField(blank=True, default='', max_length=1200),
        ),
    ]
