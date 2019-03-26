from django import forms
from django.contrib.auth.models import User
from users.models import *
from qnppr.models import *
from users.views import *

from users import config

class AddSubject(forms.ModelForm):

    class Meta:
        model = Subject
        fields =['dept', 'sem', 'subcode', 'subname']
        labels ={
            "dept": "Department", "sem": "Semester", "subcode": "Subject Code","subname": "Subject Name"
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sem'].queryset = Semester.objects.all()

        if 'dept' in self.data:
            try:
                dept_id = int(self.data.get('dept'))
                self.fields['sem'].queryset = Semester.objects.filter(dept_id_id=dept_id).order_by('sem_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['sem'].queryset = self.instance.dept.sem_set.order_by('sem_name')

    def clean_subcode(self):
        subcode = self.cleaned_data.get('subcode')
        subcode = Subject.objects.filter(subcode=subcode)
        sem = self.cleaned_data.get('sem')
        #us = request.session['user']
        #print(iid)
        print(sem)
        print(subcode)
        print(config.iid)
        if  subcode:
            raise forms.ValidationError('Subject with the same Subject Code Exist')
        return self.cleaned_data.get('subcode')

    def clean_subname(self):
        dept_name = self.cleaned_data.get('dept')
        sem_name = self.cleaned_data.get('sem')
        sub_name = self.cleaned_data.get('subname')
        dept = Department.objects.get(dept_name=dept_name)
        print(dept)
        sem = Semester.objects.get(dept_id=dept, sem_name=sem_name)
        subname = Subject.objects.filter(sem=sem, dept=dept,  subname=sub_name)
        if subname:
            raise forms.ValidationError('Subject with the same Name Exist in the chosen Semester')
        return self.cleaned_data.get('subname')

class CoMapping_form1(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['dept', 'sem']
        labels = {
            'dept': 'Department', 'sem': 'Semester'
        }

class CoMapping_form2(forms.ModelForm):
    class Meta:
        model = Co_mapping
        fields = ['sub_code', 'module', 'co_id', 'co_desc']
        labels = {
            'sub_code': 'Subject', 'co_id': 'CO', 'co_desc': 'CO Description'
        }
