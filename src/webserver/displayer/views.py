from django.shortcuts import render
from src.webserver.commons import get_records
from django.template.defaulttags import register


# Create your views here.

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def index(request):
    context = {
        'content': [
            {'option': 'validate', 'url': 'validate'},
            {'option': 'class schedule', 'url': 'class_schedule'},
            {'option': 'teachers\' schedule', 'url': 'teacher_schedule'},
            {'option': 'free class rooms', 'url': 'free_classes'}
        ]
    }
    return render(request, 'displayer/index.html', context)


def validate(request):
    return render(request, 'displayer/validate.html', get_records())


def class_schedule(request):
    context = {}
    return render(request, 'displayer/class_schedule.html', context)


def teacher_schedule(request):
    context = {}
    return render(request, 'displayer/teacher_schedule.html', context)


def free_classes(request):
    context = {}
    return render(request, 'displayer/free_classes.html', context)
