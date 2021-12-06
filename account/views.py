from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import DetailView, UpdateView

from .forms import UserLoginForm, UserRegistrationForm, UserEditForm
from .utils import send_confirmation_email
from .utils import token_generator

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            user = get_object_or_404(User, username=username)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = 'https://' + domain + reverse('account:activation', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
            email = form.cleaned_data['email']
            send_confirmation_email(email, link)
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
