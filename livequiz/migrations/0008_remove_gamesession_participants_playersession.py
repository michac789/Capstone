# Generated by Django 4.0.4 on 2022-06-18 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('livequiz', '0007_rename_game_id_gamesession_code_gamesession_game_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamesession',
            name='participants',
        ),
        migrations.CreateModel(
            name='PlayerSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playing', to=settings.AUTH_USER_MODEL)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livequiz.gamesession')),
            ],
        ),
    ]
