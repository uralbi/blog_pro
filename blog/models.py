from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from pathlib import Path
from io import BytesIO
from django.core.files import File
from django.utils.html import mark_safe

def validate_positive(value):
    if value < 0:
        raise ValidationError("Price must be a positive number.")

def image_process(image):
    width, height = 900, 900
    img = Image.open(image)
    ch_width, ch_height = img.size
    if ch_width <= 900 or ch_height <= 900:
        return
    if img.width > width or img.height > height:
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
        img.save(buffer, format='PNG', optimize=True)
        buffer.seek(0)  # Move to the beginning of the BytesIO buffer before saving
        new_img_filename = f"{img_filename}.png"
        image.save(new_img_filename, File(buffer), save=False)


class BlogPost(models.Model):
    title = models.CharField(max_length=255, verbose_name = 'Тема')
    info = models.TextField(verbose_name = 'Инфо', blank=True)
    price = models.IntegerField(blank=True, null=True, validators=[validate_positive], verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = 'Добавлен')
    updated_at = models.DateTimeField(auto_now=True, verbose_name = 'Исправлен')

    def __str__(self):
        return self.title


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