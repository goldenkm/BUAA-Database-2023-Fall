# Generated by Django 4.2.5 on 2023-11-28 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_major_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.AlterField(
            model_name='post',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='帖子创建时间'),
        ),
    ]
