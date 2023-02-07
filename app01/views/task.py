# -*- coding : utf-8 -*-            
# @Time : 2022/5/2 16:26
# @Author : SXQ
# @FileName : task
import json

from django import forms
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from app01 import models

from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            "detail": forms.TextInput
        }


def task_list(request):
    """
    任务列表
    :param request:
    :return:
    """
    # 去数据库获取所有任务(根据id降序排列)
    queryset = models.Task.objects.all().order_by('level')
    page_object = Pagination(request, queryset, page_size=3)
    form = TaskModelForm()
    context = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_str": page_object.html()
    }
    return render(request, 'task_list.html', context)


# 若为post请求则免除csrf_token认证
@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)
    data_dict = {"status": True, 'data': [11, 22, 33, 44]}
    return HttpResponse(json.dumps(data_dict))
    # return JsonResponse(data_dict)


@csrf_exempt
def task_add(request):
    # print(request.POST)
    # 1.用户发送过来的数据进行校验
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))
    data_dict = {"status": False, "error": form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
