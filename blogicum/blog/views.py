from datetime import datetime
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from .models import Post, Category


def index(request):
    """функция отображения главной страницы."""
    template_name = 'blog/index.html'
    post_list = Post.objects.filter(
        pub_date__lt=datetime.now(),
        is_published=True,
    )[:5]
    context = {
        'post_list': post_list,
    }
    return render(request, template_name, context)


def post_detail(request, id):
    """функция отображения страницы с постами."""
    template_name = 'blog/detail.html'
    post = Post.objects.select_related(Category).filter(
        pk=id,
    )
    context = {
        'post': post
    }
    return render(request, template_name, context)


def category_posts(request, category_slug):
    """функция отображения категории списка постов."""
    template_name = 'blog/category.html'
    category = Category.objects.select_related(Post).filter(slug=category_slug)
    context = {'category': category}
    return render(request, template_name, context)
