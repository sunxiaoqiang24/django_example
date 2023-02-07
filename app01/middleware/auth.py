# -*- coding : utf-8 -*-            
# @Time : 2022/5/2 9:25
# @Author : SXQ
# @FileName : auth
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):
    """
    中间件
    """

    def process_request(self, request):
        # 排除那些不要登录就能访问的页面
        if request.path_info in ["/login/", "/image/code/"]:
            return
        # 1.读取当前访问的session信息,若有说明已经登录
        info_dict = request.session.get("info")
        # print(info_dict)
        if info_dict:
            return
        # 2.没有登录过,重新回到登录页面
        return redirect("/login/")

    # def process_response(self, request, response):
    #     print("M1.走了")
    #     return response
