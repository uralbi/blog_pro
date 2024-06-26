# Generated by Django 4.2 on 2024-02-22 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_team_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'verbose_name': 'Команда', 'verbose_name_plural': 'Команда'},
        ),
        migrations.AddField(
            model_name='team',
            name='display',
            field=models.BooleanField(default=True, verbose_name='Показан'),
        ),
    ]
