from app import models
from django.contrib.auth.decorators import login_required


def get_new_notify_count(request):
    if 'info' in request.session:
        uid = request.session['info'].get('id')
        user = models.User.objects.filter(id=uid).first()
        comment_notification_id_list = models.CommentNotify.objects.filter(owner=user)
        count_new_comment = models.CommentNotification.objects.filter(
            id__in=[i.notification.id for i in comment_notification_id_list], is_new=True).all().count()
        like_notification_id_list = models.LikeNotify.objects.filter(owner=user)
        count_new_like = models.LikeNotification.objects.filter(
            id__in=[i.notification.id for i in like_notification_id_list], is_new=True).all().count()
        return {
            'count_new_comment': count_new_comment,
            'count_new_like': count_new_like,
            'count_new_all': count_new_like + count_new_comment
        }
    return {}


def get_user_info(request):
    if 'info' in request.session:
        uid = request.session['info'].get('id')
        user = models.User.objects.filter(id=uid).first()
        if user:
            return {
                'user_name': user.user_name,
                'user_image': user.image,
            }
    return {}
