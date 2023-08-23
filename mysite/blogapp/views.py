from django.views.generic import ListView

from .models import Article


class ArticleListView(ListView):
    """
    Отображает список всех доступных статей с дополнительной информацией
    """
    queryset = (
        Article.objects
        .defer('content')
        .select_related('author', 'category')
        .prefetch_related('tags')
    )
    context_object_name = 'articles'
