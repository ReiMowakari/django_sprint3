from django.shortcuts import render


def about(request):
    """функция отображения раздела 'О проекте'."""
    template_name = 'pages/about.html'
    context = {
        'title': 'О проекте',
    }
    return render(request, template_name, context)


def rules(request):
    """функция отображения раздела правил."""
    template_name = 'pages/rules.html'
    return render(request, template_name)
