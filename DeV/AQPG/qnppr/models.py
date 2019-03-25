from django.db import models
from django.contrib.auth.models import User
from users.models import *


class Semester(models.Model):
    sem_name = models.CharField(max_length=100)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.sem_name

class Subject(models.Model):
    subcode = models.CharField(max_length=100)
    subname = models.CharField(max_length=100)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    sem = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return self.subname