# Generated by Django 4.0.4 on 2022-06-18 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livequiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questiontype1',
            name='number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='questiontype1',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
