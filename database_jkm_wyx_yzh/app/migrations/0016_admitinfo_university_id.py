# Generated by Django 4.2.5 on 2023-12-02 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_rename_admitinformation_admitinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='admitinfo',
            name='university_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.university'),
            preserve_default=False,
        ),
    ]
