from django.urls import path
from qnppr.views import *
from django.contrib.auth import views as auth_views
from qnppr.views import *

urlpatterns = [
    path('add-sub/', subjectAdd, name="sub_add"),
    path('ajax/load-cities/', load_cities, name='ajax_load_sem'),
]