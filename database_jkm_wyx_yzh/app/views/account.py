from django.shortcuts import render, redirect, HttpResponse
from app.utils.model_form import LoginModelForm
from app import models
from app.utils.validation_img import check_code
from io import BytesIO
from django.contrib.auth import authenticate


def login(request):
    """登录"""
    if request.method == 'GET':
        form = LoginModelForm()
        return render(request, 'login.html', {'form': form})

    form = LoginModelForm(data=request.POST)
    if form.is_valid():
        # 校验验证码
        input_img_code = form.cleaned_data.pop('img_code')
        img_code = request.session.get('image_code', '')
        if img_code != input_img_code:
            form.add_error('img_code', '验证码错误')
            return render(request, 'login.html', {'form': form})
        # 校验用户名、密码
        # 自己实现
        print(form.cleaned_data)
        user = models.User.objects.filter(**form.cleaned_data).first()
        if not user:
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})
        # Django官方实现
        '''username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return HttpResponse("登录失败")'''
        # 用户名、密码正确
        # 网站生成随机字符串；写到用户浏览器的cookie中；再写入到session中；
        request.session['info'] = {'id': user.id, 'name': user.user_name}
        # session保存一天
        request.session.set_expiry(60 * 60 * 24)
        return redirect('/university/list/')
    return render(request, 'login.html', {'form': form})


def logout(request):
    """注销"""
    request.session.clear()
    return redirect('/login/')


def image_code(request):
    """生成图片验证码"""
    img, code_str = check_code()
    # 写入到自己的session中，以便于后续获取验证码再进行校验
    request.session['image_code'] = code_str
    # 给session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


