# Generated by Django 4.2 on 2024-02-22 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Профайл', 'verbose_name_plural': 'Профайл'},
        ),
        migrations.AddField(
            model_name='profile',
            name='company',
            field=models.CharField(default='Компания', max_length=255, verbose_name='Бренд'),
        ),
    ]