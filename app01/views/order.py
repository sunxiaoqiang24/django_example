# -*- coding : utf-8 -*-            
# @Time : 2022/5/3 11:29
# @Author : SXQ
# @FileName : order
import random
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid", "admin"]


def order_list(request):
    """
    订单列表
    :param request:
    :return:
    """
    # 降序排列
    # queryset实际上是一个对象列表
    queryset = models.Order.objects.all().order_by('-id')
    page_object = Pagination(request, queryset, page_size=3)
    form = OrderModelForm()
    context = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_str": page_object.html()
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """
    新建订单(Ajax请求)
    :param request:
    :return:
    """
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 额外增加一些不是用户输入的值
        # 随机生成(订单编号)
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        # 固定设置管理员
        # form.instance.admin_id=当前登录系统的管理员ID
        form.instance.admin_id = request.session['info']['id']
        form.save()
        return JsonResponse({"status": True})
        # return HttpResposne(json.dumps({"status": True}))
    return JsonResponse({"status": False, "error": form.errors})


def order_delete(request):
    """
    删除订单
    :param request:
    :return:
    """
    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, "error": "数据不存在"})
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    """
    获取订单详细
    :param request:
    :return:
    """
    uid = request.GET.get("uid")
    # 直接选取列并转换为字典
    row_dict = models.Order.objects.filter(id=uid).values("title", "price", "status").first()
    if not row_dict:
        return JsonResponse({"status": False, "error": "数据不存在"})
    # 构造一个字典
    result = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    """
    编辑订单
    :param request:
    :return:
    """
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "数据不存在"})
    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})
