from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(SideBar)
admin.site.register(University)
admin.site.register(Major)
admin.site.register(MajorUniversity)
admin.site.register(ExamInfo)
admin.site.register(AdmitInfo)
admin.site.register(User)
admin.site.register(CommentNotify)
admin.site.register(LikeNotify)
admin.site.register(CommentNotification)
admin.site.register(LikeNotification)
admin.site.register(Draft)
admin.site.register(TagPost)

