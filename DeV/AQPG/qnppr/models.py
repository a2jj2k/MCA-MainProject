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


class Module(models.Model):
    module_name = models.CharField(max_length=100)

    def __str__(self):
        return self.module_name

class Co(models.Model):
    co_cd_name = models.CharField(max_length=100)

    def __str__(self):
        return self.co_cd_name


class Co_mapping(models.Model):
    co_id = models.ForeignKey(Co, on_delete=models.CASCADE)
    co_desc = models.CharField(max_length=100)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    sub_code = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.co_desc

class Blooms_lvl(models.Model):
    blm_lvl_name = models.CharField(max_length=100)

    def __str__(self):
        return self.blm_lvl_name

class Blooms_keyword(models.Model):
    blm_lvl_name = models.ForeignKey(Blooms_lvl, on_delete=models.CASCADE)
    blm_verb = models.CharField(max_length=100)

    def __str__(self):
        return self.blm_verb