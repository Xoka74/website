from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView

from .forms import UserLoginForm, UserRegistrationForm, UserEdit

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:blog')
    form = UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'account/registration.html', context)


class LoginView(View):
    model = User
    template_name = 'account/login.html'

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('account:profile', pk=request.user.id)
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog:blog')
        context = {
            'form': form,
        }
        return render(request, 'account/login.html', context)

    def get(self, request):
        form = UserLoginForm()
        context = {
            'form': form,
        }
        return render(request, 'account/login.html', context)


class ProfileView(DetailView):
    model = User
    template_name = 'account/profile.html'


def logout_view(request):
    logout(request)
    return redirect('blog:blog')


class ProfileEdit(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user_data = user.get_user_data()
        form = UserEdit(user_data)

        context = {
            'user': user,
            'form': form,
        }
        return render(request, 'account/edit_profile.html', context)

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserEdit(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.phone_number = form.cleaned_data['phone_number']
            user.save()
            return redirect('account:profile', pk=pk)
        else:
            errors = form.errors
        context = {
            'user': user,
            'form': form,
            'errors': errors
        }
        return render(request, 'account/edit_profile.html', context)
