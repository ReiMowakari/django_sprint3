from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post, Category

# Константа для отображения 5 записей на главной странице.
POSTS_PER_PAGE = 5


# Функция объединения моделей.
def get_joined_models():
    return Post.objects.select_related(
        'location',
        'author',
        'category'
    )


# Функция фильтрации постов.
def get_filtered_posts(posts, **kwargs):
    return posts.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
        **kwargs
    )


def index(request):
    """функция отображения главной страницы проекта."""
    template_name = 'blog/index.html'
    posts = get_filtered_posts(get_joined_models()).order_by(
        '-pub_date')[:POSTS_PER_PAGE]
    context = {
        'posts': posts,
    }
    return render(request, template_name, context)


def post_detail(request, id):
    """функция отображения страницы с отдельной публикацией."""
    template_name = 'blog/detail.html'
    post = get_object_or_404(
        get_filtered_posts(get_joined_models()),
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
    posts = get_filtered_posts(get_joined_models(), category_id=category)
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, template_name, context)
