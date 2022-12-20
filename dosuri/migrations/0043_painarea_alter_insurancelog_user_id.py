# Generated by Django 4.1.2 on 2022-12-20 05:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import dosuri.user.models


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0042_rename_large_address_address_large_area_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PainArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(db_index=True, default=dosuri.user.models.generate_uuid, max_length=32)),
                ('name', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='insurancelog',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insurance_log', to=settings.AUTH_USER_MODEL),
        ),
    ]