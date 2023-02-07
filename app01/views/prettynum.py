# -*- coding : utf-8 -*-            
# @Time : 2022/5/1 10:06
# @Author : SXQ
# @FileName : prettynum

from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import PrettyModelForm, PrettyEditModelForm
from app01.utils.pagination import Pagination


def prettynum_list(request):
    """
    靓号列表
    :param request:
    :return:
    """
    # 定义数据搜索的条件
    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    # 先生成query_set
    query_set = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    # 创建对象
    page_object = Pagination(request, query_set)
    page_queryset = page_object.page_queryset
    # 生成页面
    page_str = page_object.html()

    context = {
        "queryset": page_queryset,
        "search_data": search_data,
        "page_str": page_str
    }

    return render(request, "prettynum_list.html", context)


def prettynum_add(request):
    """
    新建靓号
    :param request:
    :return:
    """
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "prettynum_add.html", {"form": form})
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list/')
    return render(request, 'prettynum_add.html', {"form": form})


def prettynum_edit(request, nid):
    """
    靓号编辑
    :param request:
    :param nid:
    :return:
    """
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, "prettynum_edit.html", {"form": form})
    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list/')
    return render(request, 'prettynum_edit.html', {"form": form})


def prettynum_delete(request, nid):
    """
    靓号删除
    :param request:
    :return:
    """
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/prettynum/list/')
