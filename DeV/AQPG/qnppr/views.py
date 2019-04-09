from django.shortcuts import render, redirect
from django.db import connection
from django.http import Http404, JsonResponse
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from qnppr.views import *
from qnppr.forms import *
import json
import spacy
from similarity.cosine import Cosine
nlp = spacy.load('en')
cosine = Cosine(3)

# Create your views here.

def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def subjectAdd(request):
    #form = AddSubject()
    if request.method == "POST":
        form = AddSubject(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Subject Added Successfully')
            return redirect('sub_add')
    else:
        form = AddSubject()
    return render(request, 'qnppr/add_subject.html', {'form': form})

def coMapping(request):
    if request.method == 'POST':
        form_1 = CoMapping_form1(request.POST)
        form_2 = CoMapping_form2(request.POST)
        if form_2.is_valid() and form_1.is_valid():
            form_2.save()
            messages.success(request, f'Mapping Added Successfully')
            return redirect('map_mod')
    else:
        form_1 = CoMapping_form1()
        form_2 = CoMapping_form2()
    return render(request, 'qnppr/map_subject_modules.html', {'form_1': form_1, 'form_2': form_2})


def addBloomsKeywords(request):
    if request.method =='POST':
        form = AddBloomKeyword(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Keyword Added Successfully')
            return redirect('add-blooms')
    else:
        form = AddBloomKeyword()
    return render(request, 'qnppr/add_blooms_keywords.html', {'form': form})


def addMarks(request):
    if request.method =='POST':
        form = AddMark(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Mark Added Successfully')
            return redirect('add-mark')
    else:
        form = AddMark()
    return render(request, 'qnppr/add_marks.html', {'form': form})

def addQuestions(request):
    if request.method == 'POST':
        form_1 = CoMapping_form1(request.POST)
        form_2 = AddQuestion(request.POST)
        if form_2.is_valid() and form_1.is_valid():
            form_2.save()
            messages.success(request, f'Mapping Added Successfully')
            return redirect('map_mod')
    else:
        form_1 = CoMapping_form1()
        form_2 = AddQuestion()
    return render(request, 'qnppr/add_question.html', {'form_1': form_1, 'form_2': form_2})


def load_semesters(request):
    dept_id = request.GET.get('dept')
    sem = Semester.objects.filter(dept_id_id=dept_id).order_by('sem_name')
    return render(request, 'qnppr/sem_dropdown_list.html', {'sem': sem})

def load_subjects(request):
    dept_id = request.GET.get('dept')
    print(dept_id)
    sem_id = request.GET.get('sem')
    subject = Subject.objects.filter(dept_id=dept_id,sem_id=sem_id ).order_by('subname')
    return render(request, 'qnppr/subject_dropdown_list.html', {'sub': subject})

def klevel_prediction(request):
    qns = request.GET.get('qn')
    #print("hi")
    #print(qns)
    cursor = connection.cursor()
    cursor.execute("""select * from qnppr_blooms_keyword order by blm_lvl_name_id""")
    dict = {}
    dict = dictfetchall(cursor)
    #print(dict)
    for d in dict:
        temp = str(d['blm_verb'])
        if temp.upper() in qns.upper():
            k_obj = Blooms_lvl.objects.get(id=int(d['blm_lvl_name_id']))
            #print(k_obj.blm_lvl_name)
            k_dict = {
                'k': k_obj.id
            }
            r = json.dumps(k_dict)
            #print(r)
            return JsonResponse(r, safe=False)
def whRemover(param):
    wh_words = ['who', 'what', 'how', 'when', 'Where']
    spltd_str = param.split()
    #print(type(spltd_str))
    #print(spltd_str)
    for i in wh_words:
        # print(i)
        for j in spltd_str:
            # print(j.upper())
            if i.upper() == j.upper():
                print("*******Match found*****")
                spltd_str.remove(j)

    #print(spltd_str)

    whrmvd_str = " ".join(str(x) for x in spltd_str)
    """for i in spltd_str:
        whrmvd_str = whrmvd_str + str(i) + " """

    #print(whrmvd_str)
    return whrmvd_str


def similarity_checker(request):
    #print("Inside similarity checker")
    qn_list = []
    qns = request.GET.get('qn')
    subject = request.GET.get('sub')
    module = request.GET.get('mod')
    print(qns)
    print(subject)
    print(module)

    qn_frm_usr = qns
    whrmvd_qn_frm_usr = whRemover(qn_frm_usr)
    print("From user :" + whrmvd_qn_frm_usr)
    search_doc = nlp(whrmvd_qn_frm_usr)
    search_doc_no_stop_words = nlp(' '.join([str(t) for t in search_doc if not t.is_stop]))
    cosine_prof_ip_1 = " ".join(str(x) for x in search_doc_no_stop_words)
    cosine_ip_1 = cosine.get_profile(cosine_prof_ip_1)
    #print("stripping  :  "+ cosine_prof_ip_1)

    cursor = connection.cursor()
    cursor.execute("""select * from qnppr_question where subject_id = '%s' and module_id = '%s'""" % (subject, module))
    dict = {}
    dict = dictfetchall(cursor)

    for d in dict:
        qn_frm_db = str(d['desc'])
        whrmvd_qn_frm_db = whRemover(qn_frm_db)
        print("From db :" + whrmvd_qn_frm_db)
        db_doc = nlp(whrmvd_qn_frm_db)
        db_doc_no_stop_words = nlp(' '.join([str(t) for t in db_doc if not t.is_stop]))
        cosine_prof_ip_2 = " ".join(str(x) for x in db_doc_no_stop_words)

        cosine_ip_2 = cosine.get_profile(cosine_prof_ip_2)

        cosine_sim = cosine.similarity_profiles(cosine_ip_1, cosine_ip_2)#cosine similarity measuring
        print("cosine similarity : " + str(cosine_sim))

        if cosine_sim > 0.49:
            qn_list.append(qn_frm_db)

    qn_dict_list = []
    for qn in qn_list:
        adict = {'qn': qn}
        qn_dict_list.append(adict)

    print(qn_dict_list)
    subject = Subject.objects.all()
    return render(request, 'qnppr/similar_qn_list.html', {'qnlist': qn_dict_list})