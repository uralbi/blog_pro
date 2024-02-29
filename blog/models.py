from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from pathlib import Path
from io import BytesIO
from django.core.files import File
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

def validate_positive(value):
    if value < 0:
        raise ValidationError("Price must be a positive number.")

def image_process(image):
    width, height = 600, 600
    img = Image.open(image)
    ch_width, ch_height = img.size
    if ch_width <= width or ch_height <= height:
        return
    else:
        output_size = (width, height)
        img.thumbnail(output_size)
        img_filename = Path(image.file.name).stem  # file name without the extension
        cur_w, cur_h = img.size
        img_ratio = round(cur_w / cur_h, 2)
        if img_ratio < 0.8: # Vertical cropping
            cr_size = (cur_h - cur_w) / 2.2
            top = cr_size
            bottom = cur_h - cr_size
            img = img.crop((0, top, cur_w, bottom))
        elif img_ratio > 1.6: # Horizontal cropping
            cr_size = (cur_w - cur_h) / 2.7
            left = cr_size
            right = cur_w - cr_size
            img = img.crop((left, 0, right, cur_h))

        buffer = BytesIO()
        img.save(buffer, format='WEBP', optimize=True)
        buffer.seek(0)  # Move to the beginning of the BytesIO buffer before saving
        new_img_filename = f"{img_filename}.webp"
        image.save(new_img_filename, File(buffer), save=False)


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("Автор"))
    company = models.CharField(max_length=255, default='Компания', verbose_name=_("Бренд"))
    address = models.CharField(max_length=255, verbose_name=_("Адрес"))
    phone = models.CharField(max_length=20, verbose_name=_("Телефон"))
    whatsapp_number = models.CharField(max_length=20, verbose_name=_("Вотсап"))
    email = models.EmailField(verbose_name=_("Email"))
    instagram_url = models.URLField(verbose_name=_("Инстаграм"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = 'Создан')

    class Meta:
        verbose_name = _("Профайл")
        verbose_name_plural = _("Профайл")

    def __str__(self):
        return self.author.username


class Team(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Автор'))
    name = models.CharField(max_length=255, verbose_name=_("Имя"))
    position = models.CharField(max_length=255, verbose_name=_("Должность"))
    image = models.ImageField(upload_to='blog_images/', verbose_name = 'Фото')
    display = models.BooleanField(default=True, verbose_name = 'Показан')

    def save(self, *args, **kwargs):
        if self.image:
            image_process(self.image)
        super().save(*args, **kwargs)

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="100" />')

    class Meta:
        verbose_name = _("Команда")
        verbose_name_plural = _("Команда")


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Автор'))
    title = models.CharField(max_length=255, verbose_name = 'Тема')
    info = models.TextField(verbose_name ='Инфо', blank=True)
    price = models.IntegerField(blank=True, null=True, validators=[validate_positive], verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = 'Добавлен')
    updated_at = models.DateTimeField(auto_now=True, verbose_name = 'Исправлен')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Пост")
        verbose_name_plural = _("Посты")


class BlogImage(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', verbose_name = 'Фото')

    def __str__(self):
        return f"Фото - {self.blog_post.title}"

    def save(self, *args, **kwargs):
        if self.image:
            image_process(self.image)
        super().save(*args, **kwargs)

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="100" />')

    image_tag.short_description = 'Preview'

    class Meta:
        verbose_name = _("Фото")
        verbose_name_plural = _("Фото")