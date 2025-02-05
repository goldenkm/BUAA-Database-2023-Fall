# Generated by Django 4.2.5 on 2023-12-01 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_major_university_id_major_school'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='majoruniversity',
            options={'verbose_name': '专业-学校', 'verbose_name_plural': '专业-学校'},
        ),
        migrations.AddField(
            model_name='major',
            name='english_exam',
            field=models.CharField(default=0, max_length=16, verbose_name='英语'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='major',
            name='politic_exam',
            field=models.CharField(default=1, max_length=16, verbose_name='政治'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='major',
            name='professional_exam1',
            field=models.CharField(default=1, max_length=16, verbose_name='专业课1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='major',
            name='professional_exam2',
            field=models.CharField(default=1, max_length=16, verbose_name='专业课2'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ExamSubject',
        ),
    ]
