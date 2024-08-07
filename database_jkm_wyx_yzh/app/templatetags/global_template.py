from django import template
from django.db.models import Count
from app.models import *

register = template.Library()


@register.simple_tag
def get_sidebar_list():
    return SideBar.get_sidebar()


@register.simple_tag
def get_new_post():
    return Post.objects.order_by('create_time')[:5]


@register.simple_tag
def get_hot_post():
    query_set = Like.objects.annotate(count=Count('post_id')).order_by('-count')[:5]
    ans = []
    for item in query_set:
        ans.append(Post.objects.filter(id=item.post_id).first())
    return ans


@register.simple_tag
def get_all_tags():
    return Tag.objects.all()
