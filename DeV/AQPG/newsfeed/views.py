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
from users import config

from django.http import HttpResponse
from django.views.generic import View
import datetime

from django.http import HttpResponse
from django.views.generic import View
import datetime

class PostListView(ListView):
    model = Post
    template_name = 'newsfeed/newsfeed.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['full_name'] = config.full_name
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['full_name'] = config.full_name
        return context

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['full_name'] = config.full_name
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
        context['full_name'] = config.full_name
        return context


class PostDeleteView(DeleteView):
    print("inside deleteview")
    model = Post
    success_url = '/newsfeed/'

    def get_context_data(self, **kwargs):
        context = super(PostDeleteView, self).get_context_data(**kwargs)
        context['full_name'] = config.full_name
        return context




