# -*- coding : utf-8 -*-            
# @Time : 2022/5/1 19:40
# @Author : SXQ
# @FileName : account
from io import BytesIO

from django import forms
from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm
# 使用Form
from app01.utils.code import check_code
from app01.utils.encrypt import md5
from app01.utils.form import AdminModelForm


class LoginForm(BootStrapForm):
    # 尽量与数据库中字段名一致
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )

    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        # 默认必填不为空
        required=True
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput
    )

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return md5(pwd)


def login(request):
    """
    登录
    :param request:
    :return:
    """
    title = "用户登录"
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form, "title": title})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 输入的字典
        # print(form.cleaned_data)

        # 验证码的校验(获取的同时将其剔除掉)
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, "login.html", {"form": form, "title": title})

        # 去数据库校验(clean_data中包含用户名与hd5后的密码)
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            # 添加字段错误信息
            form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form": form, "title": title})
        # 用户名与密码正确
        # 网站生成随机字符串,写到用户浏览器cookie中,再写入到session中
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
        request.session.set_expiry(60 * 60 * 24)
        return redirect("/admin/list/")
    return render(request, "login.html", {"form": form, "title": title})


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    # 将session中数据清除
    request.session.clear()
    return redirect("/login/")


class RegisterModelForm(BootStrapModelForm):
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

    def clean_username(self):
        username = self.cleaned_data.get("username")
        exists = models.Admin.objects.filter(username=username).exists()
        if exists:
            raise ValidationError("用户已存在")
        return username

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


def register(request):
    """
    用户注册
    :param request:
    :return:
    """
    title = "用户注册"
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, "register.html", {"title": title, "form": form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/login/')
    return render(request, "register.html", {"title": title, "form": form})


def image_code(request):
    """
    图片验证码
    :param request:
    :return:
    """
    # 调用函数生成图片
    img, code_string = check_code()

    # 写入到自己的session中以便后续获取验证码进行校验
    request.session['image_code'] = code_string
    # 给session设置60s超时
    request.session.set_expiry(60)

    # print(code_string)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())
