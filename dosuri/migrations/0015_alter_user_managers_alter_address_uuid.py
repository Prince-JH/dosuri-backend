# Generated by Django 4.1.2 on 2022-11-23 04:37

from django.db import migrations, models
import dosuri.common.models
import dosuri.user.model_managers


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0014_alter_user_nickname'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', dosuri.user.model_managers.DosuriUserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='address',
            name='uuid',
            field=models.CharField(db_index=True, default=dosuri.common.models.generate_uuid, max_length=32),
        ),
    ]