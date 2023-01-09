# Generated by Django 4.1.2 on 2023-01-04 04:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0061_treatmentcategory_treatmentkeyword_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlecomment',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='articlethread',
            options={'ordering': ['created_at']},
        ),
        migrations.AddField(
            model_name='articlethread',
            name='mention',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_thread_mention', to=settings.AUTH_USER_MODEL),
        ),
    ]