from rest_framework import viewsets, permissions
from .models import BlogPost
from .srzs import BlogPostSerializer
from .pagination import StandardPagination


class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination

    def get_queryset(self):
        return BlogPost.objects.prefetch_related(
            'images'
        ).order_by('-created_at')