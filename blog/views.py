from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, DeleteView, View, DetailView

from .forms import ArticleForm, TagForm, CommentForm
from .models import Article, Tag, Comment
from .utils import searching


def blog(request):
    articles = searching(request)
    tags = Tag.objects.all()

    # Пагинация
    page_amount = 3
    paginator = Paginator(articles, page_amount)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    # Контекст
    context = {
        'tags': tags,
        'page': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'previous_url': prev_url,
    }
    return render(request, 'blog/blog.html', context=context)


def all_tags(request):
    tags = Tag.objects.all()
    context = {
        'tags': tags,
    }
    return render(request, 'blog/all_tags.html', context)


def aboutme(request):
    return render(request, 'blog/aboutme.html')


class ArticleView(View):
    model = Article
    template_name = 'blog/info.html'

    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        form = CommentForm()
        context = {
            'form': form,
            'article': article,
        }
        return render(request, 'blog/info.html', context)

    def post(self, request, slug):
        # user = get_object_or_404(User, id=request.user.id)
        article = get_object_or_404(Article, slug=slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.text = form.cleaned_data['text']
            new_comment.user = request.user
            new_comment.article = article
            new_comment.save()
            return redirect('blog:info', slug=slug)
        context = {
            'form': form,
            'article': article,
        }
        return render(request, 'blog/info.html', context)


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = (
        'article.can_add_article',
    )
    model = Article
    template_name = 'blog/info.html'
    raise_exception = True

    def get(self, request):
        form = ArticleForm()
        context = {
            'form': form,
        }
        return render(request, 'blog/create_article.html', context)

    def post(self, request):
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_article = form.save()
            return redirect('blog:info', slug=new_article.slug)
        context = {
            'form': form,
        }
        return render(request, 'blog/create_article.html', context)


class ArticleUpdateView(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):

    permission_required = (
        'article.can_change_articles',
    )
    model = Article
    template_name = 'blog/update_article.html'
    form_class = ArticleForm
    raise_exception = True


class ArticleDeleteView(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    permission_required = (
        'article.can_delete_articles',
    )
    model = Article
    context_object_name = 'article'
    template_name = 'blog/delete_article.html'
    success_url = '/blog/'
    raise_exception = True


class TagDetail(DetailView):
    model = Tag
    template_name = 'blog/search_by_tag.html'


class TagCreate(LoginRequiredMixin, View, PermissionRequiredMixin):
    permission_required = (
        'tag.can_add_tag',
    )
    raise_exception = True
    model = Tag

    def get(self, request):
        form = TagForm()
        context = {
            'form': form,
        }
        return render(request, 'blog/create_tag.html', context)

    def post(self, request):
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:blog')
        context = {
            'form': form,
        }
        return render(request, 'blog/create_tag.html', context)


class TagUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = (
        'tag.can_change_tag',
    )
    model = Tag
    template_name = 'blog/update_tag.html'
    form_class = TagForm
    raise_exception = True


class TagDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = (
        'tag.can_delete_tag',
    )
    model = Tag
    context_object_name = 'tag'
    template_name = 'blog/delete_tag.html'
    success_url = '/blog/'
    raise_exception = True


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()

    return redirect('blog:info', slug=comment.article.slug)

