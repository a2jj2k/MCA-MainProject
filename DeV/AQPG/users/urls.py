from django.urls import path
from users import views
from users.views import *

urlpatterns = [
    path('', views.user_login, name='login'),
    path('success/', success, name="user_success"),
    path('add/', userAdd, name="user_add"),
    path('add-dept/', addDepartment, name="dept_add")
]