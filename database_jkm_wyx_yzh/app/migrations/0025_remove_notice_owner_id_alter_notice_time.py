# Generated by Django 4.2.5 on 2023-12-05 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_alter_user_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='owner_id',
        ),
        migrations.AlterField(
            model_name='notice',
            name='time',
            field=models.DateTimeField(auto_now=True, verbose_name='通知创建时间'),
        ),
    ]
