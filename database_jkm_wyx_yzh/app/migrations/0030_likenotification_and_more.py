# Generated by Django 4.2.5 on 2023-12-05 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_notification_is_new'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=32, verbose_name='通知内容')),
                ('time', models.DateTimeField(auto_now=True, verbose_name='通知创建时间')),
                ('is_new', models.BooleanField(default=True, verbose_name='是否是新的通知')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user', verbose_name='点赞的用户')),
            ],
        ),
        migrations.RenameModel(
            old_name='Notification',
            new_name='CommentNotification',
        ),
        migrations.RenameModel(
            old_name='Notify',
            new_name='CommentNotify',
        ),
        migrations.AlterModelOptions(
            name='commentnotify',
            options={'verbose_name': '评论通知-用户', 'verbose_name_plural': '评论通知-用户'},
        ),
        migrations.CreateModel(
            name='LikeNotify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.likenotification')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
            options={
                'verbose_name': '点赞通知-用户',
                'verbose_name_plural': '点赞通知-用户',
            },
        ),
    ]
