# Generated by Django 3.1.6 on 2021-02-23 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0007_merge_20210223_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='reason',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Misleading content'), (2, 'Discusses/insights illegal activity'), (3, 'This information is false'), (4, 'This content insights violence'), (5, 'Hate speech'), (7, 'Bullying or Harassment'), (8, 'Other...')], default=1),
        ),
        migrations.AlterField(
            model_name='vote',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Up'), (2, 'Down')], default=1),
        ),
    ]