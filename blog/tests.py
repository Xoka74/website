from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from .models import Article, Tag, Comment, gen_slug


class TestArticle(TestCase):
    def test_article_creation(self):
        time = timezone.now()
        slug = gen_slug('TestArticle')
        article = Article.objects.create(
            title='TestArticle',
            text='TestText',
            pubdate=time,
        )
        self.assertEqual(article.title, 'TestArticle')
        self.assertEqual(article.text, 'TestText')
        self.assertEqual(article.pubdate, time)
        self.assertEqual(article.slug, slug)
        self.assertEqual(str(article), article.title)
        self.assertEqual(article.get_absolute_url(), f"/blog/{slug}")


class TestTag(TestCase):
    def test_tag_creation(self):
        slug = gen_slug('TestTagTitle')
        tag = Tag.objects.create(
            title='TestTagTitle'
        )
        self.assertEqual(tag.slug, slug)
        self.assertEqual(tag.title, 'TestTagTitle')
        self.assertEqual(str(tag), 'TestTagTitle')


class TestComment(TestCase):
    def test_comment_creation(self):
        time = timezone.now()
        user = get_user_model().objects.get(username='xoka74')
        comment = Comment.objects.create(
            text='Test comment text',
            pubdate=time,
            user=user
        )

        self.assertEqual(comment.text, 'Test comment text')
        self.assertEqual(comment.pubdate, time)
        self.assertEqual(comment.user, user)
