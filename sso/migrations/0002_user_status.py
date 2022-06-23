# Generated by Django 4.0.4 on 2022-06-23 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sso', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('T5', 'SuspendedUser'), ('T4', 'User'), ('T3', 'StarUser'), ('T2', 'Admin'), ('T1', 'SuperAdmin')], default='T4', max_length=2),
        ),
    ]
