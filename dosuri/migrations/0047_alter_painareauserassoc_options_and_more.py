# Generated by Django 4.1.2 on 2022-12-20 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0046_remove_insurancelog_user_id_insurancelog_user_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='painareauserassoc',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelTable(
            name='painareauserassoc',
            table='pain_area_user_assoc',
        ),
    ]
