from django.urls import path

from archive.views import *

urlpatterns = [
    path('', archiveViewall, name='archive_list'),
    path('ajax/archive-list/', load_archive_list, name='ajax_archive_list'),

]