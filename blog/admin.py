from django.contrib import admin
from .models import BlogPost, BlogImage


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    readonly_fields = ('image_tag',)
    extra = 1  # Specifies the number of empty forms to display


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'updated_at')
    inlines = [BlogImageInline]


@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ('blog_post', 'image_tag')
    readonly_fields = ('image_tag',)