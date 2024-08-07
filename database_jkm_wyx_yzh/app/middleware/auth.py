from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, render


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        # 首先应该排除那些不需要登录就能访问的页面
        if request.path_info in ['/login/', '/image/code/', '/user/register/', '/admin/']:
            return
        info_dict = request.session.get('info')
        if info_dict:
            return
        # 没有登录
        return redirect('/login/')

