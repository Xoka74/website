from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.redirect_to_home),
    path('home/', views.home, name='home'),
]
