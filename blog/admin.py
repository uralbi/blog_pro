from django.contrib import admin, messages
from .models import BlogPost, BlogImage, Profile, Team, Tag, Experience
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.admin import AdminSite
from .forms import BlogPostAdminForm, RestrictUserForm
from django.utils.translation import gettext_lazy as _


class RestrictToUserMixin:
    restrict_to_user_field_name = 'author'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        filter_kwargs = {self.restrict_to_user_field_name: request.user}
        return qs.filter(**filter_kwargs)


class MyAdmin(AdminSite):
    site_header = _('Администрация')
    site_title = _('Админ')  # Visible on the browser's title bar
    index_title = _('Админ')  # Visible on the main admin index page

    def each_context(self, request):
        context = super().each_context(request)
        if request.user.is_authenticated:
            if request.user.is_superuser:
                context['site_header'] = _('Админ')
            elif 'datalab' in request.user.username:
                context['site_header'] = _('DATALAB')
                context['index_title'] = _('Datalab')
                context['site_title'] = _('Datalab')
        return context


class TagAdmin(admin.ModelAdmin):
    list_display = ('value',)

class ExperAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'info', 'get_tags')

    def get_tags(self, obj):
        return ", ".join([tag.value for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    readonly_fields = ('image_tag',)
    extra = 1  # Specifies the number of empty forms to display


class BlogPostAdmin(RestrictToUserMixin, admin.ModelAdmin):
    list_display = ('author', 'title', 'display_info', 'get_tags', 'price', 'created_at', 'updated_at')
    inlines = [BlogImageInline]
    form = BlogPostAdminForm

    def display_info(self, obj):
        return obj.info[:100]
    display_info.short_description = 'Инфо'


    def get_tags(self, obj):
        return ", ".join([tag.value for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'


    def get_list_display(self, request):
        if request.user.groups.filter(name__icontains='datalab').exists():
            return ('title', 'display_info', 'get_tags', 'created_at',)
        return self.list_display

    def get_form(self, request, obj=None, **kwargs):
        Form = super().get_form(request, obj, **kwargs)
        class RequestFormWrap(Form):
            def __new__(cls, *args, **kw):
                kw['request'] = request
                return Form(*args, **kw)
        return RequestFormWrap


class BlogImageAdmin(RestrictToUserMixin, admin.ModelAdmin):
    list_display = ('blog_post', 'image_tag')
    readonly_fields = ('image_tag',)
    restrict_to_user_field_name = 'blog_post__author'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "blog_post":  # This must match the ForeignKey field name in your model
            if not request.user.is_superuser:
                kwargs["queryset"] = db_field.related_model.objects.filter(author=request.user)
            else:
                kwargs["queryset"] = db_field.related_model.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProfileAdmin(RestrictToUserMixin, admin.ModelAdmin):
    list_display=('company', 'address', 'phone', 'whatsapp_number', 'email', 'instagram_url', 'created_at', )
    form = RestrictUserForm

    def get_form(self, request, obj=None, **kwargs):
        Form = super().get_form(request, obj, **kwargs)
        class RequestFormWrap(Form):
            def __new__(cls, *args, **kw):
                kw['request'] = request
                return Form(*args, **kw)
        return RequestFormWrap


class TeamAdmin(RestrictToUserMixin, admin.ModelAdmin):
    list_display=('author', 'image_tag', 'name', 'position', 'display')
    list_editable=('display',)
    form = RestrictUserForm

    def get_list_display(self, request):
        if request.user.groups.filter(name__icontains='datalab').exists():
            return ('image_tag', 'name', 'position', 'display')
        return self.list_display

    def get_form(self, request, obj=None, **kwargs):
        Form = super().get_form(request, obj, **kwargs)
        class RequestFormWrap(Form):
            def __new__(cls, *args, **kw):
                kw['request'] = request
                return Form(*args, **kw)
        return RequestFormWrap


my_admin = MyAdmin(name='myadmin')
my_admin.register(Team, TeamAdmin)
my_admin.register(BlogPost, BlogPostAdmin)
my_admin.register(BlogImage, BlogImageAdmin)
my_admin.register(Experience, ExperAdmin)
my_admin.register(Tag, TagAdmin)
my_admin.register(User, UserAdmin)
my_admin.register(Group, GroupAdmin)
my_admin.register(Profile, ProfileAdmin)
