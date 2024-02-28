from rest_framework import viewsets, permissions
from .models import BlogPost, Profile, Team
from .srzs import BlogPostSerializer, ProfileSerializer, TeamSerializer
from .pagination import StandardPagination
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination

    def get_queryset(self):
        return BlogPost.objects.filter(author__username__icontains='datalab').prefetch_related(
            'images'
        ).order_by('-created_at')

    @method_decorator(cache_page(60 * 15))  # Cache this view for 15 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Profile.objects.all()
        return queryset.filter(author__username='manager_datalab')

    @method_decorator(cache_page(60 * 15))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Team.objects.filter(display=True, author__username='manager_datalab')
        return queryset

    @method_decorator(cache_page(60 * 15))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)