# Generated by Django 4.0.4 on 2022-06-22 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livequiz', '0014_alter_questiontype1_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questiontype1',
            options={'verbose_name': 'Type 1 Question'},
        ),
        migrations.AlterOrderWithRespectTo(
            name='questiontype1',
            order_with_respect_to=None,
        ),
    ]
