# Generated by Django 4.1.2 on 2022-10-27 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dosuri', '0007_alter_hospitalcalendar_hospital'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DoctorDetail',
            new_name='DoctorDescription',
        ),
        migrations.AlterField(
            model_name='doctor',
            name='thumbnail_url',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='introduction',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='phone_no',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='hospitalcalendar',
            name='friday',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='hospitalcalendar',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_calendar', to='dosuri.hospital'),
        ),
        migrations.AlterField(
            model_name='hospitalcalendar',
            name='monday',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='hospitalcalendar',
            name='saturday',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='hospitalcalendar',
            name='sunday',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='hospitalcalendar',
            name='thursday',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='hospitalcalendar',
            name='tuesday',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='hospitalcalendar',
            name='wednesday',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
