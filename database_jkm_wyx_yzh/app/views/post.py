from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse
from app import models
from app.utils.pagination import Pagination
from app.utils.model_form import UserModelForm, PostModelForm, CommentModelForm, DraftModelForm
import json
from django.views.decorators.csrf import csrf_exempt


def post_list(request):
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict['post_name__contains'] = search_data
    query_set = models.Post.objects.filter(**data_dict)
    page = Pagination(request, queryset=query_set, page_size=10)
    context = {
        'search_data': search_data,
        'posts': page.page_queryset,
        'page_str': page.html(),
    }
    return render(request, 'post/post_list.html', context=context)


def post_detail(request, pid):
    """文章详情页"""
    post = get_object_or_404(models.Post, id=pid)
    # 查询点赞数量
    user_id = request.session['info'].get('id')
    user = models.User.objects.filter(id=user_id).first()
    # 查询评论
    comments = models.Comment.objects.filter(post_id=pid).all().order_by('-create_time')
    if request.method == 'POST':
        content = request.POST.get('content')
        comment = models.Comment(post_id=post, author=user, content=content)
        comment.save()
        message = '您的帖子 《' + post.title + '》有新的评论'
        if user.id != post.author.id:  # 自己评论自己不通知
            notification = models.CommentNotification(post_id=post, comment_id=comment, message=message)
            notification.save()
            notify = models.CommentNotify(notification=notification, owner=post.author)
            notify.save()
        return redirect('/post/' + str(post.id) + '/detail/')
    prev = models.Post.objects.filter(id__lt=pid).last()
    after = models.Post.objects.filter(id__gt=pid).first()
    like_count = models.Like.objects.filter(post_id=pid).count()
    has_liked = models.Like.objects.filter(user=user, post_id=pid)
    new_comment = CommentModelForm
    tag_ids = models.TagPost.objects.filter(post=post)
    tags = models.Tag.objects.filter(id__in=[i.id for i in tag_ids]).all()
    context = {
        'post': post,
        'prev': prev,
        'after': after,
        'like_count': like_count,
        'comments': comments,
        'new_comment': new_comment,
        'has_liked': has_liked,
        'tags': tags,
    }
    return render(request, 'post/post_detail.html', context=context)


def toggle_like(request, pid):
    # 查询点赞数量
    user_id = request.session['info'].get('id')
    user = models.User.objects.filter(id=user_id).first()
    has_liked = models.Like.objects.filter(user=user, post_id=pid)
    post = models.Post.objects.get(id=pid)
    # 根据是否已点赞，进行相应的处理
    if has_liked:
        # 取消点赞
        has_liked.delete()
        if user.id != post.author.id:
            like_notification = models.LikeNotification.objects.get(post_id=post, user=user)
            like_notify = models.LikeNotify.objects.get(notification=like_notification)
            print(like_notify)
            like_notification.delete()
            like_notify.delete()
        return HttpResponse('false')
    else:
        # 点赞
        like = models.Like(user=user, post_id=pid)
        like.save()
        message = '赞了这条帖子'
        if user.id != post.author.id:  # 自己给自己点赞不通知
            like_notification = models.LikeNotification(post_id=post, user=user, message=message)
            like_notification.save()
            like_notify = models.LikeNotify(notification=like_notification, owner=post.author)
            like_notify.save()
        return HttpResponse('success')


def post_search(request):
    """ 搜索视图 """
    keyword = request.GET.get('keyword')
    if not keyword:
        posts = models.Post.objects.all()
    else:
        posts = models.Post.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword))
    context = {
        'posts': posts
    }
    return render(request, 'post/post_list.html', context=context)


def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = models.User.objects.filter(id=request.session['info'].get('id')).first()
        if 'submit-button' in request.POST:
            form = PostModelForm(data={
                'title': title,
                'content': content,
                'author': author,
            }
            )
            if form.is_valid():
                post = form.save()
                return redirect('/post/' + str(post.id) + '/detail/')
            return render(request, 'post/post_create.html', context={'form': form})
        elif 'draft-button' in request.POST:
            draft_form = DraftModelForm(data={
                'title': title,
                'content': content,
                'author': author,
            })
            if draft_form.is_valid():
                draft_form.save()
                return redirect('/post/list/')
            return render(request, '/post/post_create.html', context={'form': draft_form})
    form = PostModelForm()
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def post_create_from_draft(request, draft_id):
    draft = models.Draft.objects.get(id=draft_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = models.User.objects.filter(id=request.session['info'].get('id')).first()
        if 'submit-button' in request.POST:
            form = PostModelForm(data={
                'title': title,
                'content': content,
                'author': author,
            }
            )
            if form.is_valid():
                post = form.save()
                # 还要把草稿删了
                draft.delete()
                return redirect('/post/' + str(post.id) + '/detail/')
            return render(request, 'post/post_create.html', context={'form': form})
        elif 'draft-button' in request.POST:
            if title:
                draft.title = title
                draft.content = content
                draft.author = author
                draft.save()
                return redirect('/user/draft/list/')
            return render(request, 'post/post_create_from_draft.html')
    form = PostModelForm(data={
        'title': draft.title,
        'content': draft.content,
        'author': draft.author
    })
    context = {
        'draft': draft,
        'form': form
    }
    return render(request, 'post/post_create_from_draft.html', context=context)


def save_tags(request):
    if request.method == 'POST':
        print(request.POST)
        post_id = request.POST.get('post_id')
        selected_tags = request.POST.getlist('selected_tags[]')
        for tag_id in selected_tags:
            post_tag = models.TagPost(post_id=post_id, tag_id=int(tag_id))
            post_tag.save()
        return JsonResponse({'message': '标签设置成功！'})
    else:
        return JsonResponse({'message': '标签设置失败！'})


