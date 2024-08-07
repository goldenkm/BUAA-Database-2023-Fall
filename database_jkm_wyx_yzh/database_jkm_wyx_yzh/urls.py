"""
URL configuration for DjangoProject2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.views import university, account, user, major, post
from django.conf import settings
from django.conf.urls.static import static
from app.utils.upload import upload_file

urlpatterns = [
    # 管理员后台
    path('admin/', admin.site.urls),
    # 登陆
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),

    # 大学
    path('university/list/', university.university_list),
    path('university/<int:uid>/major/list/', university.university_major_list),

    # 用户
    path('user/register/', user.user_register),
    path('user/profile/', user.user_profile),
    path('user/notification/center/', user.user_notification_center),
    path('user/edit/', user.user_edit),
    path('user/edit/password/', user.user_edit_password),
    path('user/post/list/', user.user_post_list),
    path('user/post/<int:post_id>/delete/', user.user_post_delete),
    path('user/draft/list/', user.user_draft_list),
    path('user/draft/<int:draft_id>/delete/', user.user_draft_delete),

    # 专业
    path('major/list/', major.major_list),
    path('major/<str:mid>/university/list/', major.major_university_list),
    path('major/<int:uid>/<str:mid>/detail/', major.major_detail_info),
    path('major/<int:uid>/<str:mid>/detail/analyze/', major.major_detail_analyze),
    path('major/<int:uid>/<str:mid>/detail/analyze/bar/', major.major_detail_analyze_bar),
    path('major/<int:uid>/<str:mid>/detail/exam/', major.major_detail_exam),
    path('major/<int:uid>/<str:mid>/detail/post/', major.major_detail_post),

    # 帖子
    path('post/list/', post.post_list),
    path('post/<int:pid>/detail/', post.post_detail),
    path('post/search/', post.post_search),
    path('post/create/', post.post_create),
    path('post/create_from/draft/<int:draft_id>/', post.post_create_from_draft),
    path('post/<int:pid>/detail/like/', post.toggle_like),
    path('post/save/tags/', post.save_tags),

    # 上传文件
    path('', include('ckeditor_uploader.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # 配置静态文件url


# 配置用户上传文件url
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "一研为定管理后台"
admin.site.index_title = "一研为定管理后台"
admin.site.site_title = "一研为定管理员登陆了"
