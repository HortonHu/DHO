from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib.auth import *


def user_login(request):
    """
    login
    """
    if request.POST:
        username = password = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_activate:
            login(request, user)
            return redirect('/')
    ctx = dict()
    ctx.update(csrf(request))
    return render(request, 'users/login.html', ctx)


def user_logout(request):
    """
    logout
    URL: /users/logout
    """
    logout(request)
    return redirect('/')




