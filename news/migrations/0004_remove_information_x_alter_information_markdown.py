# Generated by Django 4.0.4 on 2022-06-24 06:59

from django.db import migrations
import news.models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_information_x'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='information',
            name='x',
        ),
        migrations.AlterField(
            model_name='information',
            name='markdown',
            field=news.models.NonStrippingTextField(),
        ),
    ]