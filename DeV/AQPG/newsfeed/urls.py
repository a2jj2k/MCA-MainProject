from django.urls import path
from newsfeed.views import *
from .views import (

    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView
)
from . import views

urlpatterns = [
    #path('', PostListView.as_view(), name='newsfeed-home'),
    path('', postViewall, name='newsfeed-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]