from django.shortcuts import render, redirect


def redirect_to_home(request):
    return redirect('main:home', permanent=True)


def home(request):
    return render(request, 'main/home.html')



