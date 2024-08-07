from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from app import models

from app.utils.pagination import Pagination
from app.utils.model_form import MajorModelForm
from django.contrib.auth.decorators import login_required


def major_list(request):
    data_dict = {}
    search_data = request.GET.get('keyword', '')
    if search_data:
        data_dict['major_name__contains'] = search_data
    query_set = models.Major.objects.filter(**data_dict).order_by('major_id')
    page = Pagination(request, queryset=query_set, page_size=10)
    context = {
        'search_data': search_data,
        'query_set': page.page_queryset,
        'page_string': page.html(),
    }
    return render(request, 'major/major_list.html', context=context)


def major_university_list(request, mid):
    universities = models.MajorUniversity.objects.filter(major_id=mid).order_by('university_id')
    major = models.Major.objects.filter(major_id=mid).first()
    page = Pagination(request, queryset=universities, page_size=10)
    context = {
        'query_set': page.page_queryset,
        'page_string': page.html(),
        'major': major
    }
    return render(request, 'major/major_university_list.html', context=context)


def major_detail_info(request, uid, mid):
    major = models.Major.objects.filter(major_id=mid).first()
    university = models.University.objects.filter(university_id=uid).first()
    school = models.MajorUniversity.objects.filter(major=major, university_id=university).first().school
    info = models.AdmitInfo.objects.filter(major_id=mid, university_id=uid).order_by('-year', '-total_score')
    years = models.AdmitInfo.objects.order_by('-year').values_list('year', flat=True).distinct()
    print(years)
    context = {
        'university': university,
        'major': major,
        'query_set': info,
        'years': years,
        'school': school,
    }
    return render(request, 'major_detail_*/major_detail_info.html', context=context)


def major_detail_analyze(request, uid, mid):
    major = models.Major.objects.filter(major_id=mid).first()
    university = models.University.objects.filter(university_id=uid).first()
    school = models.MajorUniversity.objects.filter(major=major, university_id=university).first().school
    context = {
        'university': university,
        'major': major,
        'school': school,
    }
    return render(request, 'major_detail_*/major_detail_analyze.html', context=context)


def major_detail_analyze_bar(request, uid, mid):
    major = models.Major.objects.filter(major_id=mid).first()
    university = models.University.objects.filter(university_id=uid).first()
    min_score = models.AdmitInfo.objects.filter(major_id=major, university_id=university).order_by('score1').all()
    min_score_year = {
        '2019': min_score.filter(year=2019).first(),
        '2020': min_score.filter(year=2020).first(),
        '2021': min_score.filter(year=2021).first(),
        '2022': min_score.filter(year=2022).first(),
        '2023': min_score.filter(year=2023).first(),
    }
    series_list1 = [
        {
            'label': {
                'show': 'true',
                'position': 'top',
            },
            'type': 'bar',
            'data': [i.score1 for i in min_score_year.values()]
        }
    ]
    series_list2 = [
        {
            'label': {
                'show': 'true',
                'position': 'top',
            },
            'type': 'bar',
            'data': [i.total_score for i in min_score_year.values()]
        }
    ]
    res = {
        'status': True,
        'data': {
            'x_axis': [i for i in min_score_year.keys()],
            'series_list1': series_list1,
            'series_list2': series_list2,
        }
    }
    return JsonResponse(res)


def major_detail_exam(request, uid, mid):
    major = models.Major.objects.filter(major_id=mid).first()
    university = models.University.objects.filter(university_id=uid).first()
    exam_info = models.ExamInfo.objects.filter(major_id=mid, university_id=uid).first()
    school = models.MajorUniversity.objects.filter(major=major, university_id=university).first().school
    context = {
        'university': university,
        'major': major,
        'exam_info': exam_info,
        'school': school,
    }
    return render(request, 'major_detail_*/major_detail_exam.html', context=context)


def major_detail_post(request, uid, mid):
    major = models.Major.objects.filter(major_id=mid).first()
    university = models.University.objects.filter(university_id=uid).first()
    context = {
        'university': university,
        'major': major,
    }
    return HttpResponse('尚未开放')
