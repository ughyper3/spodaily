# Generated by Django 3.2.9 on 2021-11-21 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spodaily_api', '0015_alter_activity_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='average_session_length',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='number_of_session_per_week',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
