from django.shortcuts import render, redirect
from app import models
from app.utils.pagination import Pagination


# Create your views here.
def university_list(request):
    """ 学校列表 """
    data_dict = {}
    search_data = request.GET.get('keyword', '')
    if search_data:
        data_dict['name__contains'] = search_data
    query_set = models.University.objects.filter(**data_dict).order_by('university_id')
    page = Pagination(request, queryset=query_set, page_size=10)
    context = {
        'search_data': search_data,
        'query_set': page.page_queryset,
        'page_string': page.html(),
    }
    return render(request, 'university/university_list.html', context)


def university_major_list(request, uid):
    major_ids = models.MajorUniversity.objects.filter(university_id=uid).all()
    majors = models.Major.objects.filter(major_id__in=[item.major.major_id for item in major_ids]).order_by('major_id')
    university = models.University.objects.filter(university_id=uid).first()
    context = {
        'query_set': majors,
        'university': university,
    }
    return render(request, 'university/university_major_list.html', context)
