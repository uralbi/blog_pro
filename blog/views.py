from rest_framework import viewsets, permissions
from .models import BlogPost
from .srzs import BlogPostSerializer
from .pagination import StandardPagination


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination