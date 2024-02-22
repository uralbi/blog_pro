from django import forms
from django.contrib.auth.models import User
from .models import BlogPost


class BlogPostAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        user = self.request.user if self.request else None

        if user and not user.is_superuser:
            self.fields['author'].queryset = User.objects.filter(id=user.id)

        if user and 'datalab' in str(user.groups.all()):
            self.fields['price'].widget = forms.HiddenInput()
            self.fields['author'].initial = user.id
            self.fields['author'].widget = forms.HiddenInput()
    class Meta:
        model = BlogPost
        fields = '__all__'


class RestrictUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        user = self.request.user if self.request else None

        if user and not user.is_superuser:
            self.fields['author'].queryset = User.objects.filter(id=user.id)
            if self.fields['author']:
                self.fields['author'].initial = user.id
                self.fields['author'].widget = forms.HiddenInput()