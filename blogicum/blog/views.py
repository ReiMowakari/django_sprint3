from datetime import datetime
from django.shortcuts import render, get_object_or_404
from .models import Post, Category

# Текущая дата и время.
now = datetime.now()


def index(request):
    """функция отображения главной страницы проекта."""
    template_name = 'blog/index.html'
    post_list = Post.objects.select_related(
        'location',
        'author',
        'category'
    ).filter(
        pub_date__lte=now,
        is_published=True,
        category__is_published=True,
    ).order_by('-pub_date')[:5]
    context = {
        'post_list': post_list,
    }
    return render(request, template_name, context)


def post_detail(request, id):
    """функция отображения страницы с отдельной публикацией."""
    template_name = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.filter(
            pub_date__lte=now,
            is_published=True,
            category__is_published=True
        ),
        pk=id,
    )
    context = {
        'post': post
    }
    return render(request, template_name, context)


def category_posts(request, category_slug):
    """функция отображения страницы категории."""
    template_name = 'blog/category.html'
    # Определяем категорию по слагу. Если категории нет и неопубликована - 404.
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    # Получение списка постов по отфильтрованной категории.
    post_list = category.posts.filter(
        pub_date__lte=now,
        is_published=True,
    )
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, template_name, context)
