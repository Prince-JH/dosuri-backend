# Generated by Django 4.1.2 on 2023-02-06 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0075_alter_article_hospital'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='usernotification',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='userpointhistory',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='unread_notice',
            field=models.BooleanField(default=True),
        ),
    ]