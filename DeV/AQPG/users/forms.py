from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from users.models import *


class UserRegisterForm_user(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    """def __init__(self, *args, **kwargs):
        super(UserRegisterForm_user, self).__init__(*args, **kwargs)
        #instance = getattr(self, 'instance', None)
        #if instance and instance.pk:
        self.fields['username'].initial = "Hi"
        self.fields['username'].widget.attrs['readonly'] = True"""


    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']


        if commit:
            user.save()
        return user

    '''def clean(self):
        super(UserRegisterForm_user, self).clean()
        user = self.cleaned_data.get('username')
        try:
            match = User.objects.get(username=user)
        except:
            return self.cleaned_data['username']
        raise forms.ValidationError('User Exist')'''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_email = User.objects.filter(email=email)
        print(user_email)
        if  user_email:
            raise forms.ValidationError('Email id already exist for another User')
        return self.cleaned_data.get('email')


"""class UserRegisterForm_dept(forms.ModelForm):
    #dept_name = forms.ChoiceField(choices=Department.objects.all())
    #dept_name = forms.ComboField(choices=Department.objects.all())

    class Meta:
        model = Department
        fields = ['dept_name']
        labels = {
            "dept_name": "Department name"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dept_name'].queryset = Department.objects.all()"""

class UserProfile(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['dept_id', 'is_student', 'image']
        labels = {
            "dept_id": "Department Name",
            "image": "Profile Picture",
            "is_student": "Is Student"
        }

class AddDepartment(forms.ModelForm):
    dept_name = forms.CharField()

    class Meta:
        model = Department
        fields = ['dept_name']
        labels = {
            "dept_name": "Department Name"
        }
    def clean_dept_name(self):
        dept_name = self.cleaned_data.get('dept_name')
        dept_name = Department.objects.filter(dept_name=dept_name)
        print(dept_name)
        if  dept_name:
            raise forms.ValidationError('Department with the same name already exist')
        return self.cleaned_data.get('dept_name')