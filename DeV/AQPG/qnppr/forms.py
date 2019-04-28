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

    """def clean_dept(self):

        #print(self.cleaned_data.get('dept'))
        config.co_mapping_dept_id = self.cleaned_data.get('dept')
        #print("******")
        #print(config.co_mapping_dept_id)
        #print("############")
        return self.cleaned_data.get('dept')"""

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
        config.SUB_CUR_SLCTD=s_code
        mod_id = self.cleaned_data.get('module')
        co_id = self.cleaned_data.get('co_id')
        print(s_code)
        print(mod_id)
        #print(config.co_mapping_dept_id)
        subject = Subject.objects.get(subname=s_code)
        module = Module.objects.get(module_name=mod_id)
        co_id = Co.objects.get(co_cd_name=co_id)

        co_map = Co_mapping.objects.filter(module=module, sub_code=subject)
        if co_map:
            raise forms.ValidationError('Mapping Already Exist')
        else:
            co_id_chk = Co_mapping.objects.filter(co_id=co_id, sub_code=subject)
            if co_id_chk:
                raise forms.ValidationError('Selected CO Already mapped for another Module')
            else:
                return self.cleaned_data.get('co_id')

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

class AddMark(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['mark_disp', 'dept']

    def __init__(self, *args, **kwargs):
        super(AddMark, self).__init__(*args, **kwargs)

        # self.fields['username'].widget.attrs['disabled'] = True
        self.fields['mark_disp'].widget.attrs['type'] = "number"

    def clean_mark_disp(self):
        mrk = self.cleaned_data.get('mark_disp')
        if mrk.isdigit():
            m = int(mrk)
            if m > 0:
                return self.cleaned_data.get('mark_disp')
            else:
                raise forms.ValidationError('Invalid Mark')
        else:
            raise forms.ValidationError('Invalid Mark')


class AddQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'module', 'desc', 'fig', 'klevel', 'mark']
        labels = {'desc': 'Qn Description','fig': 'Figure', 'klevel': 'Knowledege Level'}

    def __init__(self, *args, **kwargs):
        super(AddQuestion, self).__init__(*args, **kwargs)
        self.fields['desc'].widget.attrs['rows'] = 5

    def clean_module(self):
        dept = Department.objects.get(dept_name=config.dept_id)
        print(dept)
        print("*********")
        #print(dept.id)
        print("************")
        sub_name = self.cleaned_data.get('subject')
        module = self.cleaned_data.get('module')
        module = Module.objects.get(module_name=module)
        print(module.id)
        sub_name = Subject.objects.get(dept=dept, subname=sub_name)
        print(sub_name.subcode)
        mapping_exist = Co_mapping.objects.filter(module=module, sub_code=sub_name)
        if mapping_exist:
            #raise forms.ValidationError('Module not mapped to any CO')
            return self.cleaned_data.get('module')
        else:
            #return self.cleaned_data.get('module')
            raise forms.ValidationError('Module not mapped to any CO')

class TestForm(forms.Form):
    rollno = forms.CharField(max_length=100)

    def clean_rollno(self):
        mrk = self.cleaned_data.get('rollno')
        if mrk.isdigit():
            m = int(mrk)
            if m > 0:
                return self.cleaned_data.get('rollno')
            else:
                raise forms.ValidationError('Invalid Mark')
        else:
            raise forms.ValidationError('Invalid Mark')

class Generate_qn_dep_sem_form(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['dept', 'sem']
        labels = {
            'dept': 'Department', 'sem': 'Semester'
        }

class Generate_qn_sub_form(forms.ModelForm):
    class Meta:
        model = Co_mapping
        fields = ['sub_code']
        labels = {
            'sub_code': 'Subject'
        }

    def clean_sub_code(self):
        s_code = self.cleaned_data.get('sub_code')
        config.SUB_CUR_SLCTD = s_code.subname
        print(config.SUB_CUR_SLCTD)
        print(type(config.SUB_CUR_SLCTD))
        return self.cleaned_data.get('sub_code')


class DeptSemForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['dept', 'sem']
        labels = {
            'dept': 'Department', 'sem': 'Semester'
        }



class GenerateQnPpr(forms.Form):
    c = [(0, 0),(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    c1 = [(0, 0), (2, 2)]
    exm = [('Internal', 'Internal')]
    sub_code = forms.ModelChoiceField(queryset=Subject.objects.all(), label="Subject")
    exm_type = forms.ChoiceField(choices=exm, label="Exam Type")
    exam_name = forms.CharField(max_length=100)
    mod_1_A = forms.ChoiceField(choices=c, label="Module 1")
    mod_2_A = forms.ChoiceField(choices=c, label="Module 2")
    mod_3_A = forms.ChoiceField(choices=c, label="Module 3")
    mod_4_A = forms.ChoiceField(choices=c, label="Module 4")
    mod_5_A = forms.ChoiceField(choices=c, label="Module 5")
    mod_6_A = forms.ChoiceField(choices=c, label="Module 6")

    mod_1_B = forms.ChoiceField(choices=c1, label="Module 1")
    mod_2_B = forms.ChoiceField(choices=c1, label="Module 2")
    mod_3_B = forms.ChoiceField(choices=c1, label="Module 3")
    mod_4_B = forms.ChoiceField(choices=c1, label="Module 4")
    mod_5_B = forms.ChoiceField(choices=c1, label="Module 5")
    mod_6_B = forms.ChoiceField(choices=c1, label="Module 6")


    """ module wise count checking method for PART - A  begins """
    def clean_mod_1_A(self):
        print("inside gen mca clean")
        module = Module.objects.get(module_name='Module 1')
        dept = str(config.dept_id)
        print(type(dept))
        dept = Department.objects.get(dept_name=dept)
        mark = Mark.objects.get(mark_disp='3', dept=dept)
        subject = self.cleaned_data.get('sub_code')
        print("*****************")
        print(subject)
        print("******************")
        subject = Subject.objects.get(subname=subject, dept=dept)
        cnt_DB = Question.objects.filter(subject=subject, module=module, mark=mark).count()
        print(cnt_DB)
        cnt_FE = int(self.cleaned_data.get('mod_1_A'))
        print(cnt_DB)
        if cnt_DB >= cnt_FE:
            return self.cleaned_data.get('mod_1_A')
        else:
            raise forms.ValidationError('Insufficient no.of questions')

    def clean_mod_2_A(self):
        module = Module.objects.get(module_name='Module 2')
        dept = config.dept_id

        dept = Department.objects.get(dept_name=dept)
        mark = Mark.objects.get(mark_disp='3', dept=dept)
        subject = self.cleaned_data.get('sub_code')
        subject = Subject.objects.get(subname=subject, dept=dept)
        cnt_DB = Question.objects.filter(subject=subject, module=module, mark=mark).count()
        cnt_FE = int(self.cleaned_data.get('mod_2_A'))
        print(cnt_DB)
        if cnt_DB >= cnt_FE:
            return self.cleaned_data.get('mod_2_A')
        else:
            raise forms.ValidationError('Insufficient no.of questions')

    def clean_mod_3_A(self):
        module = Module.objects.get(module_name='Module 3')
        dept = config.dept_id
        dept = Department.objects.get(dept_name=dept)
        mark = Mark.objects.get(mark_disp='3', dept=dept)
        subject = self.cleaned_data.get('sub_code')
        subject = Subject.objects.get(subname=subject, dept=dept)
        cnt_DB = Question.objects.filter(subject=subject, module=module, mark=mark).count()
        cnt_FE = int(self.cleaned_data.get('mod_3_A'))
        print(cnt_DB)
        if cnt_DB >= cnt_FE:
            return self.cleaned_data.get('mod_3_A')
        else:
            raise forms.ValidationError('Insufficient no.of questions')

    def clean_mod_4_A(self):
        module = Module.objects.get(module_name='Module 4')
        dept = config.dept_id
        dept = Department.objects.get(dept_name=dept)
        mark = Mark.objects.get(mark_disp='3', dept=dept)
        subject = self.cleaned_data.get('sub_code')
        subject = Subject.objects.get(subname=subject, dept=dept)
        cnt_DB = Question.objects.filter(subject=subject, module=module, mark=mark).count()
        cnt_FE = int(self.cleaned_data.get('mod_4_A'))
        print(cnt_DB)
        if cnt_DB >= cnt_FE:
            return self.cleaned_data.get('mod_4_A')
        else:
            raise forms.ValidationError('Insufficient no.of questions')

    def clean_mod_5_A(self):
        module = Module.objects.get(module_name='Module 5')
        dept = config.dept_id
        dept = Department.objects.get(dept_name=dept)
        mark = Mark.objects.get(mark_disp='3', dept=dept)
        subject = self.cleaned_data.get('sub_code')
        subject = Subject.objects.get(subname=subject, dept=dept)
        cnt_DB = Question.objects.filter(subject=subject, module=module, mark=mark).count()
        cnt_FE = int(self.cleaned_data.get('mod_5_A'))
        print(cnt_DB)
        if cnt_DB >= cnt_FE:
            return self.cleaned_data.get('mod_5_A')
        else:
            raise forms.ValidationError('Insufficient no.of questions')

    def clean_mod_6_A(self):
        module = Module.objects.get(module_name='Module 6')
        dept = config.dept_id
        dept = Department.objects.get(dept_name=dept)
        mark = Mark.objects.get(mark_disp='3', dept=dept)
        subject = self.cleaned_data.get('sub_code')
        subject = Subject.objects.get(subname=subject, dept=dept)
        cnt_DB = Question.objects.filter(subject=subject, module=module, mark=mark).count()
        cnt_FE = int(self.cleaned_data.get('mod_6_A'))
        print(cnt_DB)
        if cnt_DB >= cnt_FE:
            return self.cleaned_data.get('mod_6_A')
        else:
            raise forms.ValidationError('Insufficient no.of questions')

    """ module wise count checking method for PART - A  ends """

    """ module wise count checking method for PART - B  begins """

    def clean_mod_1_B(self):
        module = Module.objects.get(module_name='Module 1')
        dept = config.dept_id
        dept = Department.objects.get(dept_name=dept)
        mark = Mark.objects.get(mark_disp='6', dept=dept)
        subject = self.cleaned_data.get('sub_code')
        subject = Subject.objects.get(subname=subject, dept=dept)
        cnt_DB = Question.objects.filter(subject=subject, module=module, mark=mark).count()
        cnt_FE = int(self.cleaned_data.get('mod_1_B'))
        if cnt_DB >= cnt_FE:
            return self.cleaned_data.get('mod_1_B')
        else:
            raise forms.ValidationError('Insufficient no.of questions')

    def clean_mod_2_B(self):
        module = Module.objects.get(module_name='Module 2')
        dept = config.dept_id
        dept = Department.objects.get(dept_name=dept)
        mark = Mark.objects.get(mark_disp='6', dept=dept)
        subject = self.cleaned_data.get('sub_code')
        subject = Subject.objects.get(subname=subject, dept=dept)
        cnt_DB = Question.objects.filter(subject=subject, module=module, mark=mark).count()
        cnt_FE = int(self.cleaned_data.get('mod_2_B'))
        if cnt_DB >= cnt_FE:
            return self.cleaned_data.get('mod_2_B')
        else:
            raise forms.ValidationError('Insufficient no.of questions')

    def clean_mod_3_B(self):
        module = Module.objects.get(module_name='Module 3')
        dept = config.dept_id
        dept = Department.objects.get(dept_name=dept)
        mark = Mark.objects.get(mark_disp='6', dept=dept)
        subject = self.cleaned_data.get('sub_code')
        subject = Subject.objects.get(subname=subject, dept=dept)
        cnt_DB = Question.objects.filter(subject=subject, module=module, mark=mark).count()
        cnt_FE = int(self.cleaned_data.get('mod_3_B'))
        if cnt_DB >= cnt_FE:
            return self.cleaned_data.get('mod_3_B')
        else:
            raise forms.ValidationError('Insufficient no.of questions')

    def clean_mod_4_B(self):
        module = Module.objects.get(module_name='Module 4')
        dept = config.dept_id
        dept = Department.objects.get(dept_name=dept)
        mark = Mark.objects.get(mark_disp='6', dept=dept)
        subject = self.cleaned_data.get('sub_code')
        subject = Subject.objects.get(subname=subject, dept=dept)
        cnt_DB = Question.objects.filter(subject=subject, module=module, mark=mark).count()
        cnt_FE = int(self.cleaned_data.get('mod_4_B'))
        if cnt_DB >= cnt_FE:
            return self.cleaned_data.get('mod_4_B')
        else:
            raise forms.ValidationError('Insufficient no.of questions')

    def clean_mod_5_B(self):
        module = Module.objects.get(module_name='Module 5')
        dept = config.dept_id
        dept = Department.objects.get(dept_name=dept)
        mark = Mark.objects.get(mark_disp='6', dept=dept)
        subject = self.cleaned_data.get('sub_code')
        subject = Subject.objects.get(subname=subject, dept=dept)
        cnt_DB = Question.objects.filter(subject=subject, module=module, mark=mark).count()
        cnt_FE = int(self.cleaned_data.get('mod_5_B'))
        if cnt_DB >= cnt_FE:
            return self.cleaned_data.get('mod_5_B')
        else:
            raise forms.ValidationError('Insufficient no.of questions')

    def clean_mod_6_B(self):
        module = Module.objects.get(module_name='Module 6')
        dept = config.dept_id
        dept = Department.objects.get(dept_name=dept)
        mark = Mark.objects.get(mark_disp='6', dept=dept)
        subject = self.cleaned_data.get('sub_code')
        subject = Subject.objects.get(subname=subject, dept=dept)
        cnt_DB = Question.objects.filter(subject=subject, module=module, mark=mark).count()
        cnt_FE = int(self.cleaned_data.get('mod_6_B'))
        if cnt_DB >= cnt_FE:
            return self.cleaned_data.get('mod_6_B')
        else:
            raise forms.ValidationError('Insufficient no.of questions')

    """ module wise count checking method for PART - B  ends """