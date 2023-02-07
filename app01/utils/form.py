# -*- coding : utf-8 -*-            
# @Time : 2022/5/1 9:56
# @Author : SXQ
# @FileName : form
from django import forms
from app01 import models

from app01.utils.bootstrap import BootStrapModelForm
from django.core.validators import RegexValidator
from django.core.validators import ValidationError

from app01.utils.encrypt import md5


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(
        min_length=3,
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.UserInfo
        # depart就是depart
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]


class PrettyModelForm(BootStrapModelForm):
    # 验证：方式1(正则+字段)
    mobile = forms.CharField(
        label="手机号",
        # 1开头的第2位为3-9,后接9个数字
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # fields.exclude["level"]
        # fields = "__all__"

    # 验证：方式2(钩子方法 clean_字段名)
    def clean_mobile(self):
        # 获取用户输入的值
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        # 验证通过,用户输入的值返回
        return txt_mobile


# 编辑场景中的ModelForm
class PrettyEditModelForm(BootStrapModelForm):
    # 显示但不可改
    # mobile = forms.CharField(disabled=True, label="手机号")

    mobile = forms.CharField(
        label="手机号",
        # 1开头的第2位为3-9,后接9个数字
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    def clean_mobile(self):
        # 当前编辑那一行的ID
        # self.instance.pk

        # 获取用户输入的值
        txt_mobile = self.cleaned_data["mobile"]

        # 排除当前已存在的号码,判断是否修改成其他已存在号码
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile


class AdminModelForm(BootStrapModelForm):
    # 添加一个确认密码字段
    confirm_password = forms.CharField(
        label="确认密码",
        # 保留原密码吗,不清除
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        # 特定标签字段
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pswd = self.cleaned_data.get("password")
        # 加完密之后进行存储
        return md5(pswd)

    # 钩子方法验证密码是否一致
    def clean_confirm_password(self):
        # 此时原密码已经加完密
        pswd = self.cleaned_data.get("password")
        # 对确认密码进行加密
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pswd != confirm:
            raise ValidationError('密码不一致')
        # 返回用户输入的值(保存到数据库中就是什么)
        return confirm


# 管理员编辑的ModelForm
class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        # 不允许修改密码
        fields = ["username"]


class AdminResetModelForm(BootStrapModelForm):
    # 添加一个确认密码字段
    confirm_password = forms.CharField(
        label="确认密码",
        # 保留原密码,不清除
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["password"]
        # 特定标签字段
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pswd = self.cleaned_data.get("password")
        md5_pwd = md5(pswd)
        # 去数据库中查找是否有一致的
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError('密码不能与之前一致')
        # 加完密之后进行存储
        return md5_pwd

    # 钩子方法验证密码是否一致
    def clean_confirm_password(self):
        # 此时原密码已经加完密
        pswd = self.cleaned_data.get("password")
        # 对确认密码进行加密
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pswd != confirm:
            raise ValidationError('密码不一致')
        # 返回用户输入的值(保存到数据库中就是什么)
        return confirm
