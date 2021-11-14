from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog, name='blog'),
    path('aboutme/', views.aboutme, name='aboutme'),
    path('create/', views.ArticleCreate.as_view(), name='create_article'),
    path('tags/', views.all_tags, name='all_tags'),
    path('<str:slug>/', views.ArticleView.as_view(), name='info'),
    path('<str:slug>/update/', views.ArticleUpdateView.as_view(), name='update_article'),
    path('<str:slug>/delete/', views.ArticleDeleteView.as_view(), name='delete_article'),
    path('tags/create/', views.TagCreate.as_view(), name='create_tag'),
    path('tags/<str:slug>/', views.TagDetail.as_view(), name='tags'),
    path('tags/<str:slug>/update/', views.TagUpdateView.as_view(), name='update_tag'),
    path('tags/<str:slug>/delete/', views.TagDeleteView.as_view(), name='delete_tag'),
    path('comment/<int:comment_id>/delete', views.delete_comment, name='delete_comment')
]
