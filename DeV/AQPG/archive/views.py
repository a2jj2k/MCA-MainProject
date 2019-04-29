from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

from qnppr.models import *
from archive.models import *
from archive.forms import *

from users import config

def archiveAdd(request):
    if request.method == 'POST':
        #form = UserRegisterForm_user(request.POST)
        form = ArchiveForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Archive Successfully Added')
            print("*******")
            return redirect('add_archive')
    else:
        #u_form = UserRegisterForm_user()
        form = ArchiveForm()
        context = {
            'form': form,
            'is_superuser': str(config.is_super_user),
            'full_name': str(config.full_name),
            'is_student': str(config.is_student),
            'dept_id': str(config.dept_id)
        }
    return render(request, 'archive/add_archive.html', context)



def archiveViewall(request):
    if request.method == 'POST':
        form_1 = ArchiveForm()

        dept = Department.objects.get(dept_name=str(config.dept_id))
        archive_list = Archive.objects.filter(dept=dept)
        #print(archive_list)
        context = {
            'form_1': form_1,
            'archive_list': archive_list,
            'is_superuser': str(config.is_super_user),
            'full_name': str(config.full_name),
            'is_student': str(config.is_student),
            'dept_id': str(config.dept_id)
        }
        return render(request, 'archive/archive_list.html', context)
    else:
        form_1 = ArchiveForm()

        dept = Department.objects.get(dept_name=str(config.dept_id))
        archive_list = Archive.objects.filter(dept=dept)
        #print(archive_list)
        context = {
            'form_1': form_1,
            'archive_list': archive_list,
            'is_superuser': str(config.is_super_user),
            'full_name': str(config.full_name),
            'is_student': str(config.is_student),
            'dept_id': str(config.dept_id)
        }
        return render(request, 'archive/archive_list.html', context)


def load_archive_list(request):
    print("Inside ajaxarchivelist")
    dept = int(request.GET.get('deptId'))
    #request.GET.get
    sem = int(request.GET.get('semId'))
    subject = int(request.GET.get('subId'))
    exmtype = int(request.GET.get('exmtypId'))

    archive_list = Archive.objects.filter(dept=dept, sem=sem, subject=subject, exm_type=exmtype)

    print(archive_list)


    context = {
        'archive_list': archive_list

    }
    return render(request, 'archive/ajax_archive_list.html', context)
