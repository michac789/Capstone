# Generated by Django 4.0.4 on 2022-06-18 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('livequiz', '0006_remove_game_game_id_gamesession'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gamesession',
            old_name='game_id',
            new_name='code',
        ),
        migrations.AddField(
            model_name='gamesession',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ongoing', to='livequiz.game'),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
