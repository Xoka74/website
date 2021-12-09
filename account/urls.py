from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('profile/<pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<pk>/edit', views.ProfileEdit.as_view(), name='edit_profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.register, name='reg'),
]
