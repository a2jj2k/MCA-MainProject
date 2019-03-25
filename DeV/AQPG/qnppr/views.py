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


def load_cities(request):
    dept_id = request.GET.get('dept')
    sem = Semester.objects.filter(dept_id_id=dept_id).order_by('sem_name')
    return render(request, 'qnppr/sem_dropdown_list.html', {'sem': sem})
