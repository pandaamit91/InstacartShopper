from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    latest_question_list = {}
    context = {'latest_question_list': latest_question_list}
    return render(request, 'index.html', context)

def next(request):
    latest_question_list = {}
    context = {'latest_question_list': latest_question_list}
    return render(request, 'next.html', context)
