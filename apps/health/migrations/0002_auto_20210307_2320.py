# Generated by Django 3.1.6 on 2021-03-07 23:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='health',
            old_name='sleep_no',
            new_name='sleep',
        ),
        migrations.RenameField(
            model_name='health',
            old_name='steps_no',
            new_name='steps',
        ),
        migrations.RenameField(
            model_name='health',
            old_name='total_sleep',
            new_name='water',
        ),
        migrations.RemoveField(
            model_name='health',
            name='total_steps',
        ),
        migrations.RemoveField(
            model_name='health',
            name='total_water',
        ),
        migrations.RemoveField(
            model_name='health',
            name='water_no',
        ),
        migrations.AddField(
            model_name='health',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]