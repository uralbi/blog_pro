# Generated by Django 4.2 on 2024-02-22 15:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_alter_blogimage_options_alter_blogpost_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('whatsapp_number', models.CharField(max_length=20, verbose_name='Вотсап')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('instagram_url', models.URLField(blank=True, null=True, verbose_name='Инстаграм')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Профайл',
                'verbose_name_plural': 'Профайлы',
            },
        ),
    ]
