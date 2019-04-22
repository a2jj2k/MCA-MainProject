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
