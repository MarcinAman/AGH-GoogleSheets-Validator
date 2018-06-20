from django.shortcuts import render

from .models import *


# Create your views here.

def index(request):
    rows = Row.objects
    context = {'content': rows}
    return render(request, 'displayer/index.html', context)
