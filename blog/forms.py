from django.core.exceptions import ValidationError
from django.forms import ModelForm, SelectMultiple, DateTimeInput, Textarea, TextInput

from .models import Article, Tag, Comment


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text', 'pubdate', 'tags', 'slug']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title',
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Text',
            }),
            'pubdate': DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Publication time',
            }),
            'tags': SelectMultiple(attrs={
                'class': 'form-control',
                'placeholder': 'Tags',
            }),
            'slug': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Slug',
            }),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if Tag.objects.filter(slug__exact=new_slug).count():
            raise ValidationError(f'Slug "{new_slug}" already exists')
        return new_slug


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['title', 'slug']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title',
            }),
            'slug': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Slug',
            }),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'text',
                'cols': 10,
                'rows': 5
            }),
        }

