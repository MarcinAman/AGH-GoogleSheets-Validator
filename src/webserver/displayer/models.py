from django.db import models


# Create your models here.

class Row(models.Model):
    row_id = models.IntegerField


class Record(models.Model):
    column = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    row_id = models.ForeignKey(Row, on_delete=models.CASCADE)


class Teachers(models.Model):
    name = models.CharField(max_length=100)


class ClassRoom(models.Model):
    class_room_id = models.CharField(max_length=50)


class SingleClass(models.Model):
    title = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')

