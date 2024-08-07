from django.shortcuts import render, redirect
from app import models

from app.utils.pagination import Pagination
from app.utils.model_form import UserModelForm, EditPwdModelForm


def user_register(request):
    """ 注册用户 """
    title = '注册用户'
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user/user_register.html', {'title': title, 'form': form})

    # 用户Post提交数据，并进行校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 数据合法，保存到数据库
        form.save()
        user = models.User.objects.filter(**form.cleaned_data).first()
        if request.FILES:
            user.image = request.FILES['image']
            user.save()
        # 网站生成随机字符串；写到用户浏览器的cookie中；再写入到session中；
        request.session['info'] = {'id': user.id, 'name': user.user_name}
        # session保存一天
        request.session.set_expiry(60 * 60 * 24)
        return redirect('/university/list/')
    else:
        # 校验失败，显示错误信息
        return render(request, 'change.html', {'title': title, 'form': form})


def user_profile(request):
    nid = request.session['info'].get('id')
    user = models.User.objects.filter(id=nid).first()
    return render(request, 'user/user_profile.html', {'user': user})


def user_edit(request):
    """编辑用户"""
    uid = request.session['info'].get('id')
    user = models.User.objects.filter(id=uid).first()
    if request.method == 'GET':
        # 根据id去数据库获取要编辑的那一行数据
        context = {
            'user': user,
        }
        return render(request, 'user/user_edit.html', context=context)
    data = {
        'user_name': request.POST.get('user_name'),
        'password': user.password,
        'age': request.POST.get('age'),
        'major': request.POST.get('major'),
        'introduction': request.POST.get('introduction'),
        'gender': request.POST.get('gender'),
    }
    form = UserModelForm(data=data, instance=user)
    if form.is_valid():
        form.save()
        if request.FILES:
            user.image = request.FILES['image']
        user.save()
        return redirect('/user/profile/')
    else:
        return render(request, 'user/user_edit.html', {'form': form})


def user_edit_password(request):
    uid = request.session['info'].get('id')
    user = models.User.objects.filter(id=uid).first()
    context = {}
    if request.method == 'GET':
        return render(request, 'user/user_edit_password.html', context=context)
    form = EditPwdModelForm(data=request.POST, instance=user)
    if form.is_valid():
        form.save()
        return redirect('/user/profile/')
    context['form'] = form
    return render(request, 'user/user_edit_password.html', context=context)


def user_notification_center(request):
    uid = request.session['info'].get('id')
    user = models.User.objects.filter(id=uid).first()
    comment_notification_id_list = models.CommentNotify.objects.filter(owner=user)
    comment_notifications = models.CommentNotification.objects.filter(
        id__in=[i.notification.id for i in comment_notification_id_list]).all().order_by('-time')
    like_notification_id_list = models.LikeNotify.objects.filter(owner=user)
    like_notifications = models.LikeNotification.objects.filter(
        id__in=[i.notification.id for i in like_notification_id_list]).all().order_by('-time')

    # 更新消息的状态
    comment_notifications.filter(is_new=True).update(is_new=False)
    like_notifications.filter(is_new=True).update(is_new=False)
    context = {
        'comment_notifications': comment_notifications,
        'like_notifications': like_notifications,
    }
    return render(request, 'user/user_profile_notification_center.html', context=context)


def user_post_list(request):
    uid = request.session['info'].get('id')
    user = models.User.objects.filter(id=uid).first()
    posts = models.Post.objects.filter(author=user).all().order_by('-create_time')
    context = {
        'posts': posts
    }
    return render(request, 'user/user_post_list.html', context=context)


def user_post_delete(request, post_id):
    models.Post.objects.get(id=post_id).delete()
    return redirect('/user/post/list/')


def user_draft_list(request):
    uid = request.session['info'].get('id')
    user = models.User.objects.filter(id=uid).first()
    drafts = models.Draft.objects.filter(author=user).all().order_by('-create_time')
    context = {
        'drafts': drafts,
    }
    return render(request, 'user/user_draft_list.html', context=context)


def user_draft_delete(request, draft_id):
    models.Draft.objects.get(id=draft_id).delete()
    return redirect('/user/draft/list/')
