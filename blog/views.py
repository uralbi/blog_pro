from rest_framework import viewsets, permissions
from rest_framework.generics import ListAPIView
from .models import BlogPost, Profile, Team, Experience
from .srzs import BlogPostSerializer, ProfileSerializer, TeamSerializer
from .pagination import StandardPagination
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .srzs import ExperienceSerializer, ProfileSerializer
from rest_framework import generics


class ExperienceListView(ListAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

    @method_decorator(cache_page(60 * 20))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__value=tag)
        return queryset


class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination

    def get_queryset(self):
        return BlogPost.objects.filter(author__username__icontains='datalab').prefetch_related(
            'images'
        ).order_by('-created_at')

    @method_decorator(cache_page(60 * 20))  # Cache this view for 30 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Profile.objects.all()
        return queryset.filter(author__username='manager_datalab')

    @method_decorator(cache_page(60 * 20))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Team.objects.filter(display=True, author__username='manager_datalab')
        return queryset

    @method_decorator(cache_page(60 * 20))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)