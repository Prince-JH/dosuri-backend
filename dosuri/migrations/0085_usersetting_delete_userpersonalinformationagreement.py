# Generated by Django 4.1.2 on 2023-06-08 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import dosuri.user.models


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0084_userpersonalinformationagreement'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(db_index=True, default=dosuri.user.models.generate_uuid, max_length=32)),
                ('agree_marketing_personal_info', models.BooleanField(default=True)),
                ('agree_general_push', models.BooleanField(default=True)),
                ('agree_marketing_push', models.BooleanField(default=True)),
                ('agree_marketing_email', models.BooleanField(default=True)),
                ('agree_marketing_sms', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_setting', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UserPersonalInformationAgreement',
        ),
    ]
