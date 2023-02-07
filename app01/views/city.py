# -*- coding : utf-8 -*-            
# @Time : 2022/5/5 16:10
# @Author : SXQ
# @FileName : city
from django.shortcuts import render
from app01 import models


def city_list(request):
    """
    城市列表
    :param request:
    :return:
    """
    query_set = models.City.objects.all()
    return render(request, "city_list.html", {"queryset": query_set})
