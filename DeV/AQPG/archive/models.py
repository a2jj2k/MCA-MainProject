from django.db import models
from users.models import *
from qnppr.models import *

# Create your models here.
class ExamType(models.Model):
    exm_typ_name = models.CharField(max_length=100)

    def __str__(self):
        return self.exm_typ_name

class Archive(models.Model):
    exm_type_choices = (('Internal', 'Internal'), ('University', 'University'))
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    sem = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    exm_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    desc = models.CharField(max_length=100)
    attachment = models.FileField(upload_to='question_papers/', blank=False, null=False)

    def __str__(self):
        return self.desc