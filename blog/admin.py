from django.contrib import admin
from .models import Article, Tag
from .models import Comment


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    fields = ['title', 'text', 'tags', 'pubdate']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Comment)