from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from qnppr.views import *
from qnppr.forms import *

# Create your views here.

def subjectAdd(request):
    #form = AddSubject()
    if request.method == "POST":
        form = AddSubject(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Subject Added Successfully')
            return redirect('sub_add')
    else:
        form = AddSubject()
    return render(request, 'qnppr/add_subject.html', {'form': form})

def coMapping(request):
    if request.method == 'POST':
        form_1 = CoMapping_form1(request.POST)
        form_2 = CoMapping_form2(request.POST)
        if form_2.is_valid():
            form_2.save()
            messages.success(request, f'Mapping Added Successfully')
            return redirect('map_mod')
    else:
        form_1 = CoMapping_form1()
        form_2 = CoMapping_form2()
    return render(request, 'qnppr/map_subject_modules.html', {'form_1': form_1, 'form_2': form_2})


def load_semesters(request):
    dept_id = request.GET.get('dept')
    sem = Semester.objects.filter(dept_id_id=dept_id).order_by('sem_name')
    return render(request, 'qnppr/sem_dropdown_list.html', {'sem': sem})

def load_subjects(request):
    dept_id = request.GET.get('dept')
    sem_id = request.GET.get('sem')
    subject = Subject.objects.filter(dept_id=dept_id,sem_id=sem_id ).order_by('subname')
    return render(request, 'qnppr/subject_dropdown_list.html', {'sub': subject})