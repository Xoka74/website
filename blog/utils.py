from django.db.models import Q

from blog.models import Article


def searching(request):
    search_query = request.GET.get('search', '')
    if search_query:
        articles = Article.objects.filter(Q(title__icontains=search_query) | Q(text__icontains=search_query))
    else:
        articles = Article.objects.all()
    return articles


