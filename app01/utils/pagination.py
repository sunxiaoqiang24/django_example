# -*- coding : utf-8 -*-            
# @Time : 2022/4/30 18:17
# @Author : SXQ
# @FileName : pagination

"""
自定义分页组件
"""
from django.utils.safestring import mark_safe
from django.http.request import QueryDict
import copy


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request: 请求
        :param queryset: 符合条件的数据
        :param page_size: 分页大小
        :param page_param: page参数
        :param plus: 前后展示的页码
        """
        # 查询条件字典
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True

        self.query_dict = query_dict
        self.page_param = page_param

        page = request.GET.get(self.page_param, "1")
        # 判断是否为十进制
        if page.isdecimal():
            page = int(page)
        else:
            # 若为字符串则赋值为1
            page = 1
        # 当前页
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        # 根据用户想要访问的页码, 计算出起始与终止位置
        self.page_queryset = queryset[self.start:self.end]

        # 总条数
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div > 0:
            total_page_count += 1

        # 总页码数
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 总页码小于plus
        if self.total_page_count <= self.plus:
            start_page = 1
            end_page = self.total_page_count
        else:
            # 当前页 < 5时
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
                if end_page > self.total_page_count:
                    end_page = self.total_page_count
            else:
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    if start_page < 1:
                        start_page = 1
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []
        # 拼接上分页的页码
        # self.query_dict.setlist(self.page_param, [1])
        # 所有的参数拼接
        # self.query_dict.urlencode()

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'.format(
                self.query_dict.urlencode())
        page_str_list.append(prev)

        # 页面展示
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            nextv = '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">»</span></a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            nextv = '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">»</span></a></li>'.format(
                self.query_dict.urlencode())

        page_str_list.append(nextv)

        page_str_list = mark_safe("".join(page_str_list))

        return page_str_list
