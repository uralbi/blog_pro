from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from blog.admin import my_admin

urlpatterns = [
    path('admin/', my_admin.urls),
    path('blog1/', include('blog.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
