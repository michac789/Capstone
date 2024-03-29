# Generated by Django 4.0.4 on 2022-06-18 11:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('livequiz', '0005_remove_questiontype1_number_questiontype1_answer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='game_id',
        ),
        migrations.CreateModel(
            name='GameSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('current_question', models.IntegerField(default=1)),
                ('game_id', models.CharField(editable=False, max_length=6, unique=True)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hosted_games', to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
