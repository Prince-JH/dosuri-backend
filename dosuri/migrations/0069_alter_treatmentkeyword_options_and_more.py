# Generated by Django 4.1.2 on 2023-01-13 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0068_articlelike_one like by article'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='treatmentkeyword',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='user',
            name='tmp_review_username',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
