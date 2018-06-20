from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Teachers)
admin.site.register(Row)
admin.site.register(Record)
admin.site.register(ClassRoom)
admin.site.register(SingleClass)

