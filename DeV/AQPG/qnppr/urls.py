from django.urls import path
from qnppr.views import *
from django.contrib.auth import views as auth_views
from qnppr.views import *

urlpatterns = [
    path('add-sub/', subjectAdd, name="sub_add"),
    path('map-module/', coMapping, name="map_mod"),
    path('add-bloomskeywords/', addBloomsKeywords, name="add-blooms"),
    path('ajax/load-sems/', load_semesters, name='ajax_load_sem'),
    path('ajax/load-subs/', load_subjects, name='ajax_load_sub'),
]