from django.urls import path
from qnppr.views import *
from django.contrib.auth import views as auth_views
from qnppr.views import *

urlpatterns = [
    path('add-sub/', subjectAdd, name="sub_add"),
    path('map-module/', coMapping, name="map_mod"),
    path('add-bloomskeywords/', addBloomsKeywords, name="add-blooms"),
    path('add-mark/', addMarks, name="add_mark"),
    path('add-question/', addQuestions, name="add-qn"),
    #path('generate-qn-ppr/', generateQnPaper, name="gen-qn-ppr"),generateQnPaper_MCA
    path('generate-qn-ppr-mca/', generateQnPaper_MCA, name="gen-qn-ppr-mca"),
    path('generate-qn-ppr-mba/', generateQnPaper_MBA, name="gen-qn-ppr-mba"),
    path('generate-qn-ppr-technical/', generateQnPaper_Technical, name="gen-qn-ppr-technical"),
    path('view-subjects/', viewSubjectList, name="sub_list"),
    path('<int:id>/view-subject-details/', subjectDetails, name="view_subject_detail"),
    path('view-questions/', viewQuestionList, name="qn-list"),
    path('ajax/load-sems/', load_semesters, name='ajax_load_sem'),
    path('ajax/load-subs/', load_subjects, name='ajax_load_sub'),
    path('ajax/load-klevel-predi/', klevel_prediction, name='ajax_predi_klevel'),
    path('ajax/similarity-checker/', similarity_checker, name='ajax_similarity_checker'),
    path('ajax/subject-list/', load_subjectlist, name='ajax_sub_list'),
    path('ajax/question-list/', load_question_list, name='ajax_question_list'),
    path('test/', load_testform, name="test"),
]