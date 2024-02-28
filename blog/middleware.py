from django.contrib import messages
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class AdminWelcomeMessageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == reverse('admin:index') and request.user.is_authenticated:
             messages.info(request, 'Обновления в будут доступны через 15 мин после сохранения!')