from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from django.views import View
from django.views.generic import DetailView, UpdateView

from .forms import UserLoginForm, UserRegistrationForm, UserEditForm


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


class ProfileEdit(UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'account/edit_profile.html'


class ActivationView(View):
    def get(self, request, uidb64, token):
        return redirect('account:login')
