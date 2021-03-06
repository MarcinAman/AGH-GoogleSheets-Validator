from django.shortcuts import render
from src.webserver.commons import get_records_data, get_classroom_schedule, get_teachers_schedule,get_free_classes
from django.template.defaulttags import register


# Create your views here.

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_keys(k1):
    return k1.keys()


@register.filter
def get_values(k1):
    return k1.values()


@register.filter
def sort(content):
    content.sort()


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
    ctx = get_records_data()
    return render(request, 'displayer/validate.html', ctx)


def class_schedule(request):
    ctx = {'classrooms': get_classroom_schedule()}
    return render(request, 'displayer/class_schedule.html', ctx)


def teacher_schedule(request):
    context = {'teachers': get_teachers_schedule()}
    return render(request, 'displayer/teacher_schedule.html', context)


def free_classes(request):
    context = {'classrooms':get_free_classes()}
    return render(request, 'displayer/free_classes.html', context)
