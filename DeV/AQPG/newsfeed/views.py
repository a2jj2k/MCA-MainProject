from django.shortcuts import render
from django.db import connection
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from users.models import *

from users import config

from django.http import HttpResponse
from django.views.generic import View
import datetime

from django.http import HttpResponse
from django.views.generic import View
import datetime

def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def postViewall(request):
    #form_1 = DeptSemForm()
    #subject_list = Subject.objects.all()
    #dept = Department.objects.get(dept_name=config.dept_id)
    cursor = connection.cursor()

    if str(config.dept_id) == "ADMIN":

        cursor.execute("""select au.username,up.image,up.user_id, np.id,np.title, np.content, np.date_posted
                                from newsfeed_post np
                                left outer join auth_user au on np.author_id = au.id
                                left outer join users_profile up on up.user_id = np.author_id
                                order by np.date_posted asc""")
    else:
        dept = Department.objects.get(dept_name=config.dept_id)
        cursor.execute("""SELECT au.username,up.image, up.user_id, np.id, np.title, np.content, np.date_posted
                                    FROM users_profile up
                                    LEFT OUTER JOIN auth_user au ON au.id = up.user_id
                                    LEFT OUTER JOIN newsfeed_post np ON np.author_id = au.id
                                    WHERE up.dept_id_id = '%d' ORDER BY np.date_posted ASC""" % (dept.id))
    posts = {}
    posts = dictfetchall(cursor)
    print(posts)
    context = {
        'posts': posts,
        'is_superuser': str(config.is_super_user),
        'full_name': str(config.full_name),
        'is_student': str(config.is_student),
        'dept_id': str(config.dept_id)
    }
    return render(request, 'newsfeed/newsfeed.html', context)

"""class PostListView(ListView):
    model = Post
    #queryset = Post.objects.filter(author.user.profile.dept_id = d)
    template_name = 'newsfeed/newsfeed.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['full_name'] = config.full_name
        return context"""




class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['is_superuser'] = str(config.is_super_user)
        context['full_name'] = str(config.full_name)
        context['is_student'] = str(config.is_student)
        context['dept_id'] = str(config.dept_id)
        return context

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['is_superuser'] = str(config.is_super_user)
        context['full_name'] = str(config.full_name)
        context['is_student'] = str(config.is_student)
        context['dept_id'] = str(config.dept_id)
        return context


class PostUpdateView(UserPassesTestMixin, UpdateView):
    print("inside updateview")
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['is_superuser'] = str(config.is_super_user)
        context['full_name'] = str(config.full_name)
        context['is_student'] = str(config.is_student)
        context['dept_id'] = str(config.dept_id)
        return context


class PostDeleteView(DeleteView):
    print("inside deleteview")
    model = Post
    success_url = '/newsfeed/'

    def get_context_data(self, **kwargs):
        context = super(PostDeleteView, self).get_context_data(**kwargs)
        context['is_superuser'] = str(config.is_super_user)
        context['full_name'] = str(config.full_name)
        context['is_student'] = str(config.is_student)
        context['dept_id'] = str(config.dept_id)
        return context




