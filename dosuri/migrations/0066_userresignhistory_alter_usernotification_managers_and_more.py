# Generated by Django 4.1.2 on 2023-01-07 04:37

from django.db import migrations, models
import dosuri.user.model_managers
import dosuri.user.models


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0065_userpointhistory_usernotification'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserResignHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(db_index=True, default=dosuri.user.models.generate_uuid, max_length=32)),
                ('username', models.CharField(max_length=150)),
                ('reason', models.CharField(default='', max_length=256)),
            ],
            options={
                'db_table': 'user_resign_history',
                'ordering': ['-id'],
            },
        ),
        migrations.AlterModelManagers(
            name='usernotification',
            managers=[
                ('objects', dosuri.user.model_managers.UserNotificationManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='userpointhistory',
            managers=[
                ('objects', dosuri.user.model_managers.UserPointHistoryManager()),
            ],
        ),
    ]
