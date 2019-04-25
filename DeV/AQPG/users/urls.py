from django.urls import path
from users import views
from django.contrib.auth import views as auth_views
from users.views import *

urlpatterns = [
    path('', views.user_login, name='login'),
    #path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    #path('success/', success, name="user_success"),
    path('add-user/', userAdd, name="user_add"),
    path('add-dept/', addDepartment, name="dept_add"),
    path('view-users/', viewUserList, name="view_users"),
    path('<int:id>/view-user-details/', userDetails, name="view_user_detail"),
    path('ajax/user-list/', load_userlist, name='ajax_user_list')
]