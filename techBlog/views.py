from django.shortcuts import render
from django.http import HttpResponse
from posts.models import Post
from categories.models import Category


def homepage(request):
    """
    Homepage view that renders the main template with posts
    """
    posts = Post.objects.select_related('author', 'category').prefetch_related('tags').all()
    categories = Category.objects.all()

    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'index.html', context)


def api_documentation(request):
    """
    Simple API documentation page
    """
    return render(request, 'api_docs.html')