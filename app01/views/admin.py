# -*- coding : utf-8 -*-            
# @Time : 2022/5/1 10:23
# @Author : SXQ
# @FileName : admin
from django.shortcuts import render, redirect

from app01 import models
from app01.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm
from app01.utils.pagination import Pagination


def admin_list(request):
    """
    管理员列表
    :param request:
    :return:
    """
    # 检查用户是否已登录
    # 用户发来请求,获取cookie随机字符串,拿着字符串看session是否存在
    # 定义数据搜索的条件(固定)
    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        data_dict["username__contains"] = search_data

    # 根据搜索条件去数据库查询
    queryset = models.Admin.objects.filter(**data_dict)
    page_object = Pagination(request, queryset, page_size=3)
    page_queryset = page_object.page_queryset
    page_str = page_object.html()

    context = {
        'queryset': page_queryset,
        'search_data': search_data,
        'page_str': page_str
    }

    return render(request, 'admin_list.html', context)


def admin_add(request):
    """
    添加管理员
    :param request:
    :return:
    """
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'change.html', {"title": title, "form": form})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"title": title, "form": form})


def admin_edit(request, nid):
    """
    编辑管理员
    :param request:
    :param nid:
    :return:
    """
    row_object = models.Admin.objects.filter(id=nid).first()
    # 如果数据不存在
    if not row_object:
        # return render(request, "error.html", {"msg": "数据不存在"})
        return redirect("/admin/list/")

    title = "编辑管理员"
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, "change.html", {"title": title, "form": form})
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"title": title, "form": form})


def admin_delete(request, nid):
    """
    删除管理员
    :param request:
    :param nid:
    :return:
    """
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


def admin_reset(request, nid):
    """
    密码重置
    :param request:
    :param nid:
    :return:
    """
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/admin/list/")
    title = "重置密码-{}".format(row_object.username)
    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, "change.html", {"title": title, "form": form})
    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"title": title, "form": form})
