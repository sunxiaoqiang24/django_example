# -*- coding : utf-8 -*-            
# @Time : 2022/5/4 11:04
# @Author : SXQ
# @FileName : upload
import os

from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from app01 import models
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm


def upload_list(request):
    """
    文件上传
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, "upload_list.html")
    # # 请求体中数据
    # print(request.POST)
    # # 文件中数据
    # print(request.FILES)
    file_object = request.FILES.get("avatar")
    print(file_object.name)
    f = open(file_object.name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    # 将图片文件路径写入到数据库
    models.Boss.objects.create()
    return HttpResponse("上传成功！")


class UpForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']
    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


def upload_form(request):
    """
    上传form
    :param request:
    :return:
    """
    title = "Form上传"
    if request.method == "GET":
        form = UpForm()
        return render(request, 'upload_form.html', {"title": title, "form": form})
    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        print(form.cleaned_data)
        # 读取图片内容,写入到文件夹中并获取文件路径
        img_object = form.cleaned_data.get("img")

        # 创建文件路径(绝对路径)
        # media_path = os.path.join(settings.MEDIA_ROOT, img_object.name)
        # 相对路径
        media_path = os.path.join('media', img_object.name)

        f = open(media_path, mode='wb')
        for chunk in img_object.chunks():
            f.write(chunk)
        f.close()
        # 将图片文件路径写入到数据库
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=media_path
        )
        return HttpResponse("上传成功")
    return render(request, 'upload_form.html', {"title": title, "form": form})


class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = '__all__'


def upload_modelform(request):
    """
    上传modelform
    :param request:
    :return:
    """
    title = "ModelForm"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, "upload_form.html", {"form": form, "title": title})
    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse('上传成功')
    return render(request, "upload_form.html", {"form": form, "title": title})

