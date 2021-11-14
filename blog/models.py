from time import time

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Article(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    tags = models.ManyToManyField('Tag', blank=True, related_name='articles')
    pubdate = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(verbose_name='Slug', max_length=50, unique=True, blank=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)

        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/blog/{self.slug}"

    class Meta:
        ordering = ['-pubdate']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(verbose_name='Slug', max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)

        super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/blog/tags/{self.slug}"


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='user', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='comment', on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    pubdate = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user}'s comment"

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
