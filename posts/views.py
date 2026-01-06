from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from .models import Post
from .serializers import PostSerializer, PostListSerializer
from .permissions import IsAuthorOrReadOnly
from categories.models import Category
from django.db.models import Q


User = get_user_model()


class PostListView(generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__id', 'author__id']
    search_fields = ['title', 'summary', 'body']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']  # Default ordering: newest first
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # For authenticated users, show all posts
        # For unauthenticated users, show all posts as well (as per requirements)
        return Post.objects.select_related('author', 'category').prefetch_related('tags').all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        # The author is automatically set to the current user in the serializer
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related('author', 'category').prefetch_related('tags')
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method in ['GET']:
            # Allow anyone to view a post
            permission_classes = []
        else:
            # For other operations, use the default permissions (IsAuthorOrReadOnly)
            permission_classes = [IsAuthorOrReadOnly]
        
        return [permission() for permission in permission_classes]