# Generated by Django 4.1.2 on 2022-12-17 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import dosuri.hospital.models


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0038_hospitaluserassoc_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='HospitalSearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(db_index=True, default=dosuri.hospital.models.generate_uuid, max_length=32)),
                ('word', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_search', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hospital_search',
                'ordering': ['-id'],
            },
        ),
    ]
