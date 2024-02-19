from django.contrib import admin
from .models import BlogPost, BlogImage
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.admin import AdminSite


class MyAdmin(AdminSite):
    site_header = 'Администрация'  # Visible on admin login and header
    site_title = 'Админ'  # Visible on the browser's title bar
    index_title = 'Админ'  # Visible on the main admin index page

my_admin = MyAdmin(name='myadmin')


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    readonly_fields = ('image_tag',)
    extra = 1  # Specifies the number of empty forms to display


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'updated_at')
    inlines = [BlogImageInline]


class BlogImageAdmin(admin.ModelAdmin):
    list_display = ('blog_post', 'image_tag')
    readonly_fields = ('image_tag',)

my_admin.register(BlogPost, BlogPostAdmin)
my_admin.register(BlogImage, BlogImageAdmin)
my_admin.register(User, UserAdmin)
my_admin.register(Group, GroupAdmin)