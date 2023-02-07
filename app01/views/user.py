# -*- coding : utf-8 -*-            
# @Time : 2022/5/1 10:06
# @Author : SXQ
# @FileName : user
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import UserModelForm
from app01.utils.pagination import Pagination


def user_list(request):
    """
    用户列表
    :param request:
    :return:
    """
    # 获取所有的用户列表
    queryset = models.UserInfo.objects.all()

    # for obj in queryset:
    #     print(obj.id, obj.name, obj.password, obj.age, obj.account, obj.create_time.strftime("%Y-%m-%d"),
    #           obj.gender, obj.get_gender_display(), obj.depart_id, obj.depart.title)
    # 根据choices中元组编号获取值
    # obj.get_gender_display()
    # 根据id自动去关联表中获取哪一行数据depart对象
    # obj.depart.title
    page_object = Pagination(request, queryset, page_size=3)
    context = {
        "page_str": page_object.html(),
        "queryset": page_object.page_queryset
    }
    return render(request, "user_list.html", context)


def user_add(request):
    """
    添加用户
    :param request:
    :return:
    """
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, "user_add.html", context)
    # 获取用户提交的数据
    user = request.POST.get('user')
    password = request.POST.get('password')
    age = request.POST.get('age')
    account = request.POST.get('account')
    create_time = request.POST.get('create_time')
    gender = request.POST.get('gender')
    depart_id = request.POST.get('depart')

    # 添加到数据库中
    models.UserInfo.objects.create(name=user, password=password, age=age,
                                   account=account, create_time=create_time,
                                   gender=gender, depart_id=depart_id)
    return redirect("/user/list/")


def user_model_form_add(request):
    """
    添加用户（ModelForm版本）
    :param request:
    :return:
    """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})
    # 用POST提交数据,数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法保存到数据库
        form.save()
        return redirect("/user/list/")
    else:
        return render(request, "user_model_form_add.html", {'form': form})


def user_edit(request, nid):
    """
    编辑用户
    :param request:
    :return:
    """
    row_object = models.UserInfo.objects.filter(id=nid).first()
    print(type(row_object))
    if request.method == "GET":
        # 根据ID去数据库获取编辑的那一行数据
        # 默认获取一行数据并直接显示
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {'form': form})

    # 数据校验,并将用户提交的数据进行更新
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 想要在用户输入以外增加值
        # form.instance.字段名=值
        # 默认保存的用户输入的所有数据
        form.save()
        return redirect("/user/list/")
    return render(request, "user_edit.html", {'form': form})


def user_delete(request, nid):
    """
    删除用户
    :param request:
    :param nid:
    :return:
    """
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")
