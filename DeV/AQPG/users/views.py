from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from users.forms import *
from users.models import *
from users import config

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#global iid

def welcomeEmailSndr(email, first_name, last_name, username, pswd):
    email_user = 'mail.aqpg@gmail.com'
    email_password = '7559955251@Aqpg'
    email_send = email

    subject = 'Welcome to AQPG System'

    try:

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        name = first_name+" "+last_name

        body = """Hi """+name+""",\nWelcome To AQPG\n\nThe complete system for Automated Question Paper generation\n\n\nUsername : """+username+"""\nPassword : """+pswd+"""\n\n\nThanks & Regards\nTeam AQPG\n*** Enfield Technologies ***"""
        msg.attach(MIMEText(body,'plain'))

        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email_user,email_password)


        server.sendmail(email_user,email_send,text)
        server.quit()
    except Exception as e :
        print("No internet Connection")
        print(e)


def profileDisplay(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'is_superuser': str(config.is_super_user),
        'full_name': str(config.full_name),
        'is_student': str(config.is_student),
        'dept_id': str(config.dept_id)
    }

    return render(request, 'users/profile.html', context)


def user_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        #request.session['user'] = user.username
        #config.iid=user.username
        #print(config.iid)

        #prof = Profile.objects.get(user=user.id)
        #print(prof.dept_id)

        if user:
            prof = Profile.objects.get(user=user.id)
            config.iid = user.username
            config.full_name = user.first_name + " " + user.last_name
            config.is_super_user = str(user.is_superuser)
            config.is_student = prof.is_student
            config.dept_id = prof.dept_id
            #print("******")
            print(config.iid)
            print(config.full_name)
            print(config.is_super_user)
            print(config.is_student)
            print(type(config.is_student))
            print(config.dept_id)
            #print("********")
            context = {
                'is_superuser': str(config.is_super_user),
                'full_name': str(config.full_name),
                'is_student': str(config.is_student),
                'dept_id': str(config.dept_id)
            }
            login(request, user)
            return HttpResponseRedirect(reverse('newsfeed-home'), context)
            #return render(request, "users/home.html", context)
        else:
            #context["error"] = "Invalid credentials !"
            messages.error(request, 'Invalid credentials !')
            #return render(request, "users/login.html", context)
            return redirect('login')
    else:
        return render(request, "users/login.html")

def user_logout(request):
    if request.method == "GET":
        print("hi")
        logout(request)
        return HttpResponseRedirect(reverse('login'))
    #else:
        #return HttpResponseRedirect(reverse('login'))

def success(request):
    context = {}
    context['user'] = request.user
    context['dept'] = str(config.dept_id)
    return render(request, 'users/home.html', context)

def userAdd(request):
    if request.method == 'POST':
        u_form = UserRegisterForm_user(request.POST)
        p_form = UserProfile(request.POST, request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            username = u_form.cleaned_data.get('username')
            password = 'Enfield@123'
            first_name = u_form.cleaned_data.get('first_name')
            last_name = u_form.cleaned_data.get('last_name')
            email = u_form.cleaned_data.get('email')
            user = u_form.save()
            profile = p_form.save(commit=False)
            profile.user = user
            profile.save()

            welcomeEmailSndr(email, first_name, last_name, username, password)

            messages.success(request, f'User Successfully Registered')
            print("*******")
            return redirect('user_add')
    else:
        u_form = UserRegisterForm_user()
        p_form = UserProfile()
        context = {
            'u_form': u_form,
            'p_form': p_form,
            'is_superuser': str(config.is_super_user),
            'full_name': str(config.full_name),
            'is_student': str(config.is_student),
            'dept_id': str(config.dept_id)
        }
    return render(request, 'users/add_user.html', context)

def addDepartment(request):
    if request.method == 'POST':
        form = AddDepartment(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Department Added Successfully')
            return redirect('dept_add')


    else:
        form = AddDepartment()
        context = {
            'form': form,
            'is_superuser': str(config.is_super_user),
            'full_name': str(config.full_name),
            'is_student': str(config.is_student),
            'dept_id': str(config.dept_id)
        }
    return render(request, 'users/add_department.html', context)

def viewUserList(request):
    form_1 = UserProfile()
    #user_list = User.objects.all()
    pro_list = Profile.objects.select_related('user').filter(is_student=False)
    print(pro_list)
    for i in pro_list:
        print(i.image)
        print(i.user.username)
    context = {
        'form_1': form_1,
        'pro_list': pro_list,
        'is_superuser': str(config.is_super_user),
        'full_name': str(config.full_name),
        'is_student': str(config.is_student),
        'dept_id': str(config.dept_id)
    }
    return render(request, 'users/user_list.html', context)

def userDetails(request, id):
    if request.method == 'GET':
        user_obj = User.objects.get(id=id)
        user_detail = Profile.objects.get(user=user_obj)
        print(user_detail)
        context = {
            'user_obj': user_obj,
            'is_superuser': str(config.is_super_user),
            'full_name': str(config.full_name),
            'is_student': str(config.is_student),
            'dept_id': str(config.dept_id)
        }
        return render(request, 'users/user_details.html', context)
    else:
        return render(request, 'users/user_details.html')

def load_userlist(request):
    dept_id = request.GET.get('dept')
    #sem = Semester.objects.filter(dept_id_id=dept_id).order_by('sem_name')
    pro_list = Profile.objects.filter(dept_id=dept_id)
    context = {
        'pro_list': pro_list,
        'is_superuser': str(config.is_super_user),
        'full_name': str(config.full_name),
        'is_student': str(config.is_student),
        'dept_id': str(config.dept_id)

    }
    return render(request, 'users/ajax_user_list.html', context)





