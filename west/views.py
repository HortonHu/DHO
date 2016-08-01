# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template.context_processors import csrf
from west.models import Character

from django import forms


class CharacterForm(forms.Form):
    name = forms.CharField(max_length=200)


def staff(request):
    staff_list = Character.objects.all()
    return render(request, 'west/templay.html', {'staffs': staff_list})


def templay(request):
    context = dict()
    context['label'] = 'Hello world!'
    return render(request, 'west/templay.html', context)


def investigate(request):
    if request.POST:
        form = CharacterForm(request.POST)
        if form.is_valid():
            submitted = form.cleaned_data['name']
            new_record = Character(name=submitted)
            new_record.save()
    form = CharacterForm
    ctx = dict()
    ctx.update(csrf(request))
    all_record = Character.objects.all()
    ctx['staff'] = all_record
    ctx['form'] = form
    return render(request, 'west/investigate.html', ctx)