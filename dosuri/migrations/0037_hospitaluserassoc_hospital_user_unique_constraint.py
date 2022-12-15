# Generated by Django 4.1.2 on 2022-12-15 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0036_alter_hospitaluserassoc_options_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='hospitaluserassoc',
            constraint=models.UniqueConstraint(fields=('hospital', 'user'), name='hospital_user_unique_constraint'),
        ),
    ]
