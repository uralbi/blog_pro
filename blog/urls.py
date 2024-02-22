from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'blog'

router = DefaultRouter()
router.register(r'posts', BlogPostViewSet, basename='blogpost')
router.register(r'datalab_profile', ProfileViewSet)
router.register(r'datalab_team', TeamViewSet)

urlpatterns = [
    path('', include(router.urls)),
]