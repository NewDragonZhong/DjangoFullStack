#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import copy
import datetime
import json

from django.shortcuts import render, HttpResponse
from django.db.models import F

from web import models
from web.forms.home import IndexForm
from web.views import account

from backend.utils.pager import Pagination
from backend.utils.response import BaseResponse, StatusCodeEnum
from backend import commons



# 论坛页面 主函数
def testForum(request,page):
    """
        主页
    :param request:
    :return:
    """
    if request.method == 'GET':
        # page = request.GET.get('page', 1)


        news_count = models.News.objects.all().count()

        pagin = Pagination(page,news_count)

        str_news = models.News.objects.all().values()[pagin.start:pagin.end]


        return render(request, 'testForum.html', {'news_list': str_news, 'pagin':pagin})




# 性能测试主函数
def testPerformance(request):
    """
    将前端发来的数据进行处理，并且返回给前端需要的数据
    :param request:
    :return:
    """

    return render(request,'testPerformance.html',{})


# 自动化测试主函数
def testauto(request):
    """
    将前端发来的数据进行处理，并且返回给前端需要的数据
    :param request:
    :return:
    """

    return render(request,'testauto.html',{})



# 报告页面 主函数
def testReport(request,page):
    """
        测试报告发送主页
    :param request:
    :return:
    """
    if request.method == 'GET':

        news_count = models.News.objects.all().count()

        pagin = Pagination(page,news_count)

        str_news = models.News.objects.all().values()[pagin.start:pagin.end]


        return render(request, 'testReport.html', {'news_list': str_news, 'pagin':pagin})




#"---------------------*******************-------------------"
# 以下是测试页面

from change_chouti.settings import BASE_DIR  # 导入系统的根路径

def test_upload(req):
    if req.method == 'POST':
        file_obj = req.FILES.get('file')
        f = open(os.path.join(BASE_DIR,'statics','upload',file_obj.name),'wb')
        print(file_obj,type(file_obj))

        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        print("文件存储已完成！")

    return render(req, 'test.html', locals())
