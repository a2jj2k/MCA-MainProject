from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from users.forms import *
from users import config

#global iid

def about(request):
    #cursor = connection.cursor()
    #cursor.execute("""select * from blog_post""")
    #dict = {}
    #dict = dictfetchall(cursor)
    #print(dict)
    '''context = {
        # 'posts': Post.objects.all()
         'posts' : dict
    }'''
    #return render(request, 'blog/about.html', {'title': 'About'})
    return render(request, 'users/login.html')

def user_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        request.session['user'] = user.username
        config.iid=user.username
        print(config.iid)

        #prof = Profile.objects.get(user=user.id)
        #print(prof.dept_id)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('user_success'))
        else:
            #context["error"] = "Invalid credentials !"
            messages.error(request, 'Invalid credentials !')
            #return render(request, "users/login.html", context)
            return redirect('login')
    else:
        return render(request, "users/login.html")

def user_logout(request):
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect(reverse('login'))

def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'users/home.html', context)

def userAdd(request):
    if request.method == 'POST':
        u_form = UserRegisterForm_user(request.POST)
        p_form = UserProfile(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            profile = p_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, f'User Successfully Registered')
            print("*******")
            return redirect('user_add')
    else:
        u_form = UserRegisterForm_user()
        p_form = UserProfile()
        #u_form.fields['username'].attrs['readonly'] = True
    return render(request, 'users/add_user.html', {'u_form': u_form, 'p_form': p_form})

def addDepartment(request):
    if request.method == 'POST':
        form = AddDepartment(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Department Added Successfully')
            return redirect('dept_add')


    else:
        form = AddDepartment()
    return render(request, 'users/add_department.html', {'form': form})



