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

    def clean_dept(self):

        #print(self.cleaned_data.get('dept'))
        config.co_mapping_dept_id = self.cleaned_data.get('dept')
        print("******")
        print(config.co_mapping_dept_id)
        print("############")
        return self.cleaned_data.get('dept')

class CoMapping_form2(forms.ModelForm):
    class Meta:
        model = Co_mapping
        fields = ['sub_code', 'module', 'co_id', 'co_desc']
        labels = {
            'sub_code': 'Subject', 'co_id': 'CO', 'co_desc': 'CO Description'
        }

    def clean_co_id(self):
        #dept_name = self.cleaned_data.get('dept')
        s_code = self.cleaned_data.get('sub_code')
        mod_id = self.cleaned_data.get('module')
        co_id = self.cleaned_data.get('co_id')
        print(s_code)
        print(mod_id)
        print(config.co_mapping_dept_id)
        subject = Subject.objects.get(subname=s_code)
        module = Module.objects.get(module_name=mod_id)
        co_id = Co.objects.get(co_cd_name=co_id)

        co_map = Co_mapping.objects.filter(module=module, sub_code=subject)
        if co_map:
            raise forms.ValidationError('Mapping Already Exist')
        return self.cleaned_data.get('co_id')

class AddBloomKeyword(forms.ModelForm):
    class Meta:
        model = Blooms_keyword
        fields = ['blm_lvl_name', 'blm_verb']
        labels = {
            'blm_lvl_name': 'Knowledge Level', 'blm_verb': 'Blooms Verb'
        }

    def clean_blm_verb(self):
        klevel = self.cleaned_data.get('blm_lvl_name')
        verb = self.cleaned_data.get('blm_verb')
        klevel = Blooms_lvl.objects.get(blm_lvl_name=klevel)
        verb = Blooms_keyword.objects.filter(blm_lvl_name=klevel, blm_verb=verb)
        #print(user_email)
        if verb:
            raise forms.ValidationError('Blooms verb already Exist in the Selected Knowledge level')
        return self.cleaned_data.get('blm_verb')