# Generated by Django 4.2 on 2024-02-29 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_tag_blogpost_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='posts', to='blog.tag', verbose_name='Теги'),
        ),
    ]
