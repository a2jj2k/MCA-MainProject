from django.shortcuts import render, redirect
from django.db import connection
from django.http import Http404, JsonResponse
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from qnppr.views import *
from qnppr.forms import *
from users.models import *
from users import config
import json
import spacy
import random
import datetime
from similarity.cosine import Cosine
nlp = spacy.load('en')
cosine = Cosine(3)

from django.http import HttpResponse
from django.views.generic import View
import datetime

from qnppr.utils import *





# Create your views here.

def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def fisheyates(ary):
    a = len(ary)
    b = a-1
    for d in range(b, 0, -1):
        e = random.randint(0, d)
        if e == d:
            continue
        ary[d], ary[e] = ary[e], ary[d]
    return ary

def chooser(names, limit):
    """ Function that choose random qn id's without repeatition """
    container = []
    i = 0
    while i < limit:
        #random.shuffle(names)
        names = fisheyates(names)
        # print (random.choice(names))
        temp = (random.choice(names))
        if temp in container:
            random.shuffle(names)
        else:
            container.append(temp)
            random.shuffle(names)
            i = i + 1
    return container


def trimmer(ids):
    """ Function that trims and prepares the query input ids """
    q = ""
    for i in ids:
        q = q + str(i) + ","
    q = q[0:len(q) - 1]
    return (q)

def tableFormater(lis):
    blooms_tbl = []

    for f in lis:
        k1 = 0
        k2 = 0
        k3 = 0
        k4 = 0
        k5 = 0
        k5 = 0
        k6 = 0
        if str(f['blm_lvl_name']) == 'K1':
            k1 = int(f['mark_disp'])
            k2 = 0
            k3 = 0
            k4 = 0
            k5 = 0
            k6 = 0
        elif str(f['blm_lvl_name']) == 'K2':
            k1 = 0
            k2 = int(f['mark_disp'])
            k3 = 0
            k4 = 0
            k5 = 0
            k6 = 0
        elif str(f['blm_lvl_name']) == 'K3':
            k1 = 0
            k2 = 0
            k3 = int(f['mark_disp'])
            k4 = 0
            k5 = 0
            k6 = 0
        elif str(f['blm_lvl_name']) == 'K4':
            k1 = 0
            k2 = 0
            k3 = 0
            k4 = int(f['mark_disp'])
            k5 = 0
            k6 = 0
        elif str(f['blm_lvl_name']) == 'K5':
            k1 = 0
            k2 = 0
            k3 = 0
            k4 = 0
            k5 = int(f['mark_disp'])
            k6 = 0
        else:
            k1 = 0
            k2 = 0
            k3 = 0
            k4 = 0
            k5 = 0
            k6 = int(f['mark_disp'])
        temp = {
            'qn': int(f['qn']),
            'k1': k1,
            'k2': k2,
            'k3': k3,
            'k4': k4,
            'k5': k5,
            'k6': k6

        }
        blooms_tbl.append(temp)
    return blooms_tbl


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
        context={
            'form': form,
            'is_superuser': config.is_super_user,
            'full_name': config.full_name,
            'is_student': config.is_student
        }
    return render(request, 'qnppr/add_subject.html', context)

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
        context = {
            'form_1': form_1,
            'form_2': form_2,
            'is_superuser': config.is_super_user,
            'full_name': config.full_name,
            'is_student': config.is_student
        }
        print(context)
    return render(request, 'qnppr/map_subject_modules.html', {
                                                'form_1': form_1,
                                                'form_2': form_2,
                                                'is_superuser': config.is_super_user,
                                                'full_name': config.full_name,
                                                'is_student': config.is_student})
    #return render(request, 'qnppr/map_subject_modules.html',context)


def addBloomsKeywords(request):
    if request.method =='POST':
        form = AddBloomKeyword(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Keyword Added Successfully')
            return redirect('add-blooms')
    else:
        form = AddBloomKeyword()
        context = {
            'form': form,
            'is_superuser': config.is_super_user,
            'full_name': config.full_name,
            'is_student': config.is_student
        }
    return render(request, 'qnppr/add_blooms_keywords.html', context)


def addMarks(request):
    if request.method =='POST':
        form = AddMark(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Mark Added Successfully')
            return redirect('add-mark')
    else:
        form = AddMark()
        context = {
            'form': form,
            'is_superuser': config.is_super_user,
            'full_name': config.full_name,
            'is_student': config.is_student
        }

    return render(request, 'qnppr/add_marks.html', context)

def addQuestions(request):
    if request.method == 'POST':
        form_1 = CoMapping_form1(request.POST)
        form_2 = AddQuestion(request.POST, request.FILES)
        if form_2.is_valid() and form_1.is_valid():
            #print(request.FILES['fig'])
            form_2.save()
            messages.success(request, f'Question Added Successfully')
            return redirect('add-qn')
    else:
        form_1 = CoMapping_form1()
        form_2 = AddQuestion()
        context = {
            'form_1': form_1,
            'form_2': form_2,
            'is_superuser': config.is_super_user,
            'full_name': config.full_name,
            'is_student': config.is_student
        }
    return render(request, 'qnppr/add_question.html', context)

"""def generateQnPaper(request):
    if str(config.dept_id) == 'MCA':
        form_1 = GenerateQnPpr()
        form_2 = Generate_qn_dep_sem_form()
        form_3 = Generate_qn_sub_form()
        return render(request, 'qnppr/generate_question_paper_mca.html', {'form_1': form_1, 'form_2': form_2, 'form_3': form_3})"""

def viewQuestionList(request):
    if request.method == 'POST':
        question_list = Question.objects.all()
        context = {
            'question_list': question_list
        }
        return render(request, 'qnppr/question_list.html', context)
    else:
        #form_1 = CoMapping_form1()
        #form_2 = AddQuestion()
        question_list = Question.objects.all()
        context = {
            'question_list': question_list
        }
    return render(request, 'qnppr/question_list.html', context)

def viewSubjectList(request):
    form_1 = DeptSemForm()
    subject_list = Subject.objects.all()
    context = {
        'form_1': form_1,
        'subject_list': subject_list
    }
    return render(request, 'qnppr/subject_list.html', context)

def subjectDetails(request, id):
    if request.method == 'GET':
        sub_obj = Subject.objects.get(id=id)
        cursor = connection.cursor()
        cursor.execute("""SELECT qm.module_name, qc.co_cd_name, qcm.co_desc
                            FROM qnppr_co_mapping qcm 
                            LEFT OUTER JOIN qnppr_module qm ON qm.id = qcm.module_id
                            LEFT OUTER JOIN qnppr_co qc ON qc.id = qcm.co_id_id
                            WHERE qcm.sub_code_id = '%d'"""%(id))
        dict = {}
        dict = dictfetchall(cursor)
        print(dict)
        context = {
            'sub_obj': sub_obj,
            'co_obj': dict
        }
        return render(request, 'qnppr/subject_details.html', context)
    else:
        return render(request, 'qnppr/subject_details.html')

def load_subjectlist(request):
    print("Inside ajaxsubjectlist")
    dept_id = request.GET.get('dept')
    sem_id = request.GET.get('sem')
    print(type(dept_id))
    print(dept_id)
    print(type(sem_id))
    print(sem_id)

    #sem = Semester.objects.filter(dept_id_id=dept_id).order_by('sem_name')
    subject_list = Subject.objects.filter(dept=dept_id, sem=sem_id)
    print(subject_list)
    context = {
        'subject_list': subject_list

    }
    return render(request, 'qnppr/ajax_subject_list.html', context)



def generateQnPaper_MCA(request):
    if request.method =='POST':
        form_1 = GenerateQnPpr(request.POST)
        form_2 = Generate_qn_dep_sem_form(request.POST)
        form_3 = Generate_qn_sub_form(request.POST)
        exam_type = request.POST['exm_type']
        subject = int(request.POST['sub_code'])
        sub = str(subject)

        randomlypkdqns_parta = []
        randomlypkdqns_partb = []


        if exam_type == 'Internal':
            mod1_qncnt_a = int(request.POST['mod_1_A'])
            mod2_qncnt_a = int(request.POST['mod_2_A'])
            mod3_qncnt_a = int(request.POST['mod_3_A'])
            mod4_qncnt_a = int(request.POST['mod_4_A'])
            mod5_qncnt_a = int(request.POST['mod_5_A'])
            mod6_qncnt_a = int(request.POST['mod_6_A'])
            #tot_cnt_parta = mod1_qncnt_a + mod2_qncnt_a + mod3_qncnt_a + mod4_qncnt_a + mod5_qncnt_a + mod6_qncnt_a
            #print(tot_cnt_parta)
            mod1_qncnt_b = int(request.POST['mod_1_B'])
            mod2_qncnt_b = int(request.POST['mod_2_B'])
            mod3_qncnt_b = int(request.POST['mod_3_B'])
            mod4_qncnt_b = int(request.POST['mod_4_B'])
            mod5_qncnt_b = int(request.POST['mod_5_B'])
            mod6_qncnt_b = int(request.POST['mod_6_B'])
            #tot_cnt_partb = mod1_qncnt_b + mod2_qncnt_b + mod3_qncnt_b + mod4_qncnt_b + mod5_qncnt_b + mod6_qncnt_b
            #print(tot_cnt_partb)
            cur_mod_1 = connection.cursor()
            cur_mod_2 = connection.cursor()
            cur_mod_3 = connection.cursor()
            cur_mod_4 = connection.cursor()
            cur_mod_5 = connection.cursor()
            cur_mod_6 = connection.cursor()

            ###################### code for choosing PART-A qn for internal exam begins here #########################

            cur_mod_1.execute("""SELECT  * FROM qnppr_question WHERE module_id = 1 AND mark_id = 1 
                                AND subject_id = '%d'"""%(subject))
            res_mod1 = dictfetchall(cur_mod_1)
            #print("*********")
            #print(res_mod1)
            #print("***********")
            qn_mod1 = []
            for r in res_mod1:
                qn_mod1.append(r['id'])
            #print("############")
            #print(qn_mod1)
            #print("###############")



            cur_mod_2.execute("""SELECT  * FROM qnppr_question WHERE module_id = 2 AND mark_id = 1 
                                AND subject_id = '%d'"""%(subject))
            res_mod2 = dictfetchall(cur_mod_2)
            # print("*********")
            # print(res_mod1)
            # print("***********")
            qn_mod2 = []
            for r in res_mod2:
                qn_mod2.append(r['id'])
            #print("############")
            #print(qn_mod2)
            #print("###############")


            cur_mod_3.execute("""SELECT  * FROM qnppr_question WHERE module_id = 3 AND mark_id = 1 
                                            AND subject_id = '%d'""" % (subject))
            res_mod3 = dictfetchall(cur_mod_3)
            # print("*********")
            # print(res_mod1)
            # print("***********")
            qn_mod3 = []
            for r in res_mod3:
                qn_mod3.append(r['id'])
            #print("############")
            #print(qn_mod3)
            #print("###############")


            cur_mod_4.execute("""SELECT  * FROM qnppr_question WHERE module_id = 4 AND mark_id = 1 
                                                        AND subject_id = '%d'""" % (subject))
            res_mod4 = dictfetchall(cur_mod_4)
            # print("*********")
            # print(res_mod1)
            # print("***********")
            qn_mod4 = []
            for r in res_mod4:
                qn_mod4.append(r['id'])
            # print("############")
            # print(qn_mod4)
            # print("###############")


            cur_mod_5.execute("""SELECT  * FROM qnppr_question WHERE module_id = 5 AND mark_id = 1 
                                                                    AND subject_id = '%d'""" % (subject))
            res_mod5 = dictfetchall(cur_mod_5)
            # print("*********")
            # print(res_mod1)
            # print("***********")
            qn_mod5 = []
            for r in res_mod5:
                qn_mod5.append(r['id'])
            # print("############")
            # print(qn_mod4)
            # print("###############")


            cur_mod_6.execute("""SELECT  * FROM qnppr_question WHERE module_id = 6 AND mark_id = 1 
                                                                                AND subject_id = '%d'""" % (subject))
            res_mod6 = dictfetchall(cur_mod_6)
            # print("*********")
            # print(res_mod1)
            # print("***********")
            qn_mod6 = []
            for r in res_mod6:
                qn_mod6.append(r['id'])
            #print("############")
            #print(qn_mod6)
            #print("###############")


            randomlypkdqns_parta = randomlypkdqns_parta + chooser(qn_mod1, mod1_qncnt_a)
            #print("random")
            #print(randomlypkdqns_parta)
            randomlypkdqns_parta = randomlypkdqns_parta + chooser(qn_mod2, mod2_qncnt_a)
            #print(randomlypkdqns_parta)
            randomlypkdqns_parta = randomlypkdqns_parta + chooser(qn_mod3, mod3_qncnt_a)
            #print(randomlypkdqns_parta)
            randomlypkdqns_parta = randomlypkdqns_parta + chooser(qn_mod4, mod4_qncnt_a)
            #print(randomlypkdqns_parta)
            randomlypkdqns_parta = randomlypkdqns_parta + chooser(qn_mod5, mod5_qncnt_a)
            #print(randomlypkdqns_parta)
            randomlypkdqns_parta = randomlypkdqns_parta + chooser(qn_mod6, mod6_qncnt_a)
            #print(randomlypkdqns_parta)

            slctd_ids_parta = trimmer(randomlypkdqns_parta)
            #print(slctd_ids_parta)

            #query = """select qn_desc,blm_lvl from qns_tbl where qn_code in (" + slctd_ids_parta + ")"""
            query = """SELECT qq.desc, qb.blm_lvl_name, qm.mark_disp, qc.co_cd_name,qq.fig
                        FROM qnppr_question qq
                        LEFT OUTER JOIN qnppr_blooms_lvl qb ON qb.id = qq.klevel_id
                        LEFT OUTER JOIN qnppr_mark qm ON qm.id = qq.mark_id
                        LEFT OUTER JOIN qnppr_co_mapping qcm ON qcm.module_id = qq.module_id
                        LEFT OUTER JOIN qnppr_co qc ON qc.id = qcm.co_id_id
                        WHERE qq.id in (""" + slctd_ids_parta + """) AND qq.subject_id =""" + sub
            #print(query)
            cursor = connection.cursor()
            cursor.execute(query)
            result_part_A = dictfetchall(cursor)
            final_result_part_A = []

            c = 1
            for r in result_part_A:
                temp ={
                    'qn': c,
                    'desc': r['desc'],
                    'blm_lvl_name': r['blm_lvl_name'],
                    'mark_disp': r['mark_disp'],
                    'co_cd_name': r['co_cd_name'],
                    'fig': r['fig']

                }
                c = c + 1
                final_result_part_A.append(temp)


            #print(final_result_part_A)


            #print(final_result_part_A)

            ##################### code for choosing PART-A qn for internal exam ends here #############################

            """************************************************************************"""

            #################### code for choosing PART-B qn for internal exam begins here ############################

            cur_mod_1.execute("""SELECT  * FROM qnppr_question WHERE module_id = 1 AND mark_id = 3 
                                            AND subject_id = '%d'""" % (subject))
            res_mod1 = dictfetchall(cur_mod_1)
            # print("*********")
            # print(res_mod1)
            # print("***********")
            qn_mod1 = []
            for r in res_mod1:
                qn_mod1.append(r['id'])
            # print("############")
            # print(qn_mod1)
            # print("###############")

            cur_mod_2.execute("""SELECT  * FROM qnppr_question WHERE module_id = 2 AND mark_id = 3
                                            AND subject_id = '%d'""" % (subject))
            res_mod2 = dictfetchall(cur_mod_2)
            # print("*********")
            # print(res_mod1)
            # print("***********")
            qn_mod2 = []
            for r in res_mod2:
                qn_mod2.append(r['id'])
            # print("############")
            # print(qn_mod2)
            # print("###############")

            cur_mod_3.execute("""SELECT  * FROM qnppr_question WHERE module_id = 3 AND mark_id = 3 
                                                        AND subject_id = '%d'""" % (subject))
            res_mod3 = dictfetchall(cur_mod_3)
            # print("*********")
            # print(res_mod1)
            # print("***********")
            qn_mod3 = []
            for r in res_mod3:
                qn_mod3.append(r['id'])
            # print("############")
            # print(qn_mod3)
            # print("###############")

            cur_mod_4.execute("""SELECT  * FROM qnppr_question WHERE module_id = 4 AND mark_id = 3
                                                                    AND subject_id = '%d'""" % (subject))
            res_mod4 = dictfetchall(cur_mod_4)
            # print("*********")
            # print(res_mod1)
            # print("***********")
            qn_mod4 = []
            for r in res_mod4:
                qn_mod4.append(r['id'])
            # print("############")
            # print(qn_mod4)
            # print("###############")

            cur_mod_5.execute("""SELECT  * FROM qnppr_question WHERE module_id = 5 AND mark_id = 3
                                                                                AND subject_id = '%d'""" % (subject))
            res_mod5 = dictfetchall(cur_mod_5)
            # print("*********")
            # print(res_mod1)
            # print("***********")
            qn_mod5 = []
            for r in res_mod5:
                qn_mod5.append(r['id'])
            # print("############")
            # print(qn_mod4)
            # print("###############")

            cur_mod_6.execute("""SELECT  * FROM qnppr_question WHERE module_id = 6 AND mark_id = 3 
                                                                                            AND subject_id = '%d'""" % (
                subject))
            res_mod6 = dictfetchall(cur_mod_6)
            # print("*********")
            # print(res_mod1)
            # print("***********")
            qn_mod6 = []
            for r in res_mod6:
                qn_mod6.append(r['id'])
            # print("############")
            # print(qn_mod6)
            # print("###############")

            randomlypkdqns_partb = randomlypkdqns_partb + chooser(qn_mod1, mod1_qncnt_b)
            #print("random")
            #print(randomlypkdqns_partb)
            randomlypkdqns_partb = randomlypkdqns_partb + chooser(qn_mod2, mod2_qncnt_b)
            #print(randomlypkdqns_partb)
            randomlypkdqns_partb = randomlypkdqns_partb + chooser(qn_mod3, mod3_qncnt_b)
            #print(randomlypkdqns_partb)
            randomlypkdqns_partb = randomlypkdqns_partb + chooser(qn_mod4, mod4_qncnt_b)
            #print(randomlypkdqns_partb)
            randomlypkdqns_partb = randomlypkdqns_partb + chooser(qn_mod5, mod5_qncnt_b)
            #print(randomlypkdqns_partb)
            randomlypkdqns_partb = randomlypkdqns_partb + chooser(qn_mod6, mod6_qncnt_b)
            #print(randomlypkdqns_partb)

            slctd_ids_partb = trimmer(randomlypkdqns_partb)
            #print(slctd_ids_partb)


            query = """SELECT qq.desc, qb.blm_lvl_name, qm.mark_disp, qc.co_cd_name,qq.fig 
                                    FROM qnppr_question qq
                                    LEFT OUTER JOIN qnppr_blooms_lvl qb ON qb.id = qq.klevel_id
                                    LEFT OUTER JOIN qnppr_mark qm ON qm.id = qq.mark_id
                                    LEFT OUTER JOIN qnppr_co_mapping qcm ON qcm.module_id = qq.module_id
                                    LEFT OUTER JOIN qnppr_co qc ON qc.id = qcm.co_id_id
                                    WHERE qq.id in (""" + slctd_ids_partb + """) AND qq.subject_id =""" + sub
            #print(query)
            cursor = connection.cursor()
            cursor.execute(query)
            result_part_B = dictfetchall(cursor)
            final_result_part_B = []

            for r in result_part_B:
                temp ={
                    'qn': c,
                    'desc': r['desc'],
                    'blm_lvl_name': r['blm_lvl_name'],
                    'mark_disp': r['mark_disp'],
                    'co_cd_name': r['co_cd_name'],
                    'fig': r['fig']

                }
                c = c + 1
                final_result_part_B.append(temp)



            #print(final_result_part_B)
            final_blooms_tbl = tableFormater(final_result_part_A)
            final_blooms_tbl = final_blooms_tbl + tableFormater(final_result_part_B)

            total_k1 = 0
            total_k2 = 0
            total_k3 = 0
            total_k4 = 0
            total_k5 = 0
            total_k6 = 0

            for i in final_blooms_tbl:
                total_k1 = total_k1 + i['k1']
                total_k2 = total_k2 + i['k2']
                total_k3 = total_k3 + i['k3']
                total_k4 = total_k4 + i['k4']
                total_k5 = total_k5 + i['k5']
                total_k6 = total_k6 + i['k6']
                print(i)

            print(total_k1, total_k2, total_k3, total_k4, total_k5, total_k6)

            total_k1 = round((total_k1/42)*100,4)
            total_k2 = round((total_k2/42)*100,4)
            total_k3 = round((total_k3/42)*100,4)
            total_k4 = round((total_k4/42)*100,4)
            total_k5 = round((total_k5/42)*100,4)
            total_k6 = round((total_k6/42)*100,4)

            print(total_k1, total_k2, total_k3, total_k4, total_k5, total_k6)

            tempo = {
                'qn': 'Percentage',
                'k1': total_k1,
                'k2': total_k2,
                'k3': total_k3,
                'k4': total_k4,
                'k5': total_k5,
                'k6': total_k6

            }
            final_blooms_tbl.append(tempo)
            for i in final_blooms_tbl:
                print(i)

            print(final_result_part_A)
            context = {
                'part_A': final_result_part_A,
                'part_B': final_result_part_B,
                'blooms_tbl': final_blooms_tbl
            }
            pdf = render_to_pdf('qnppr/generated_qnppr_mca_internal.html', context)
            #return render(request, 'qnppr/generated_qnppr_mca_internal.html', context)
            return HttpResponse(pdf, content_type='application/pdf')

            """*****************************************************************************"""

            ########################### code for choosing PART-B qn for internal exam ends here ####################################


        """cursor = connection.cursor()
        cursor.execute('''select * from qnppr_question''')
        a = dictfetchall(cursor)
        print(a)
        print("*****************************************************************************")
        q = []
        for d in a:
            q.append(d['desc'])
        print(q)
        t = request.POST['mod_1_A']
        print(t)"""
    else:
        form_1 = GenerateQnPpr()
        form_2 = Generate_qn_dep_sem_form()
        form_3 = Generate_qn_sub_form()
        context = {
            'form_1': form_1,
            'form_2': form_2,
            'form_3': form_3,
            'is_superuser': config.is_super_user,
            'full_name': config.full_name,
            'is_student': config.is_student
        }
    return render(request, 'qnppr/generate_question_paper_mca.html', context)


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

def load_testform(request):
    if request.method =='POST':
        form = TestForm(request.POST)
        """if form.is_valid():
            form.save()
            messages.success(request, f'Mark Added Successfully')
            return redirect('add-mark')"""
    else:
        form = TestForm()
    return render(request, 'qnppr/testform.html', {'form': form})

"""class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
             'today': datetime.date.today(),
             'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        pdf = render_to_pdf('blog/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')"""