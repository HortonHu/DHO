# -*- coding:utf-8 -*-


from django.http import HttpResponse


def first_page(request):
    return HttpResponse("<h1>hello world</h1>")
