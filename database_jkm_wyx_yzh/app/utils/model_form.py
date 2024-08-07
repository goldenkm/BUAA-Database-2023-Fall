from app import models
from django import forms
from django.forms import widgets as wid
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app.utils.bootstrap import BootstrapModelForm
from app.utils.encrypt import md5
from ckeditor.widgets import CKEditorWidget


class LoginModelForm(BootstrapModelForm):
    img_code = forms.CharField(label='验证码')

    class Meta:
        model = models.User
        fields = ['user_name', 'password']
        widgets = {
            'user_name': forms.TextInput,
            'password': forms.PasswordInput,
            'img_code': forms.TextInput
        }


class UserModelForm(forms.ModelForm):
    # 为了添加约束条件可以在这里重写字段（例如min_length只能在这约束）
    user_name = forms.CharField(min_length=2, label='用户名')
    # 校验数据
    #   -方法1
    password = forms.CharField(label='密码',
                               validators=[RegexValidator('^[a-zA-Z0-9]{6,}+$', '密码只能由至少6位的字母或数字组成')])

    # 添加插件只能这么添加，不知道为什么
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，给它添加样式
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'input', 'placeholder': field.label}
            if name == 'image':
                field.widget.attrs['type'] = 'file'

    class Meta:
        model = models.User
        fields = ['user_name', 'password', 'major', 'introduction', 'age', 'gender', 'introduction', 'image']

    # 校验数据
    #   -方法2
    def clean_age(self):
        txt_age = self.cleaned_data['age']  # 用户传入的数据
        if txt_age < 18 or txt_age > 30:
            raise ValidationError('年龄范围错误')
        # 验证通过，把用户输入的数据返回
        return txt_age

    # 用户不允许重名的功能
    def clean_name(self):
        # 当前编辑的那一行的id（pk = primary key）
        # self.instance.pk
        input_name = self.cleaned_data['user_name']
        if models.UserInfo.objects.exclude(id=self.instance.pk).filter(name=input_name).exists():
            raise ValidationError('姓名重复')
        return input_name


class MajorModelForm(BootstrapModelForm):
    class Meta:
        model = models.Major
        fields = ['major_id', 'major_name']


class PostModelForm(BootstrapModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'content', 'author']
        widgets = {
            'content': CKEditorWidget()
        }


class DraftModelForm(forms.ModelForm):
    class Meta:
        model = models.Draft
        fields = ['title', 'content', 'author']
        widgets = {
            'content': CKEditorWidget()
        }


class CommentModelForm(BootstrapModelForm):
    class Meta:
        model = models.Comment
        fields = ['content']
        widgets = {
            'content': CKEditorWidget()
        }


class EditPwdModelForm(forms.ModelForm):
    password = forms.CharField(label='密码',
                               validators=[RegexValidator('^[a-zA-Z0-9]{6,}+$', '密码只能由至少6位的字母或数字组成')])
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = models.User
        fields = ['password', 'confirm_password']

    # 如果加了一个表中没有的属性，就只能重写总的clean方法
    def clean(self):
        cleaned_data = super(EditPwdModelForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        print(confirm_password, 111)
        if password != confirm_password:
            raise ValidationError('两次密码不一致')
        return cleaned_data

# class NoticeModelForm(forms.ModelForm):
