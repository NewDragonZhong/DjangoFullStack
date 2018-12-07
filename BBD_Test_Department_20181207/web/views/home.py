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



def small_talk(request,page):
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


        return render(request, 'small_talk.html', {'news_list': str_news, 'pagin':pagin})



def index(request,page):
    """
        测试报告发送主页
    :param request:
    :return:
    """
    if request.method == 'GET':

        news_count = models.News.objects.all().count()

        pagin = Pagination(page,news_count)

        str_news = models.News.objects.all().values()[pagin.start:pagin.end]


        return render(request, 'index.html', {'news_list': str_news, 'pagin':pagin})






def comment(req):
    """
    评论的ajax请求
    :param req:
    :return:
    """
    response = {"status":False,"data":{},"code":200,"message":"成功"}


    if req.method == "GET":
        num = req.GET.get("nid")

        username_info ={}
        user_info_list = []
        #
        # print(user['username'])

        comment_list = models.Comment.objects.filter(news_id=num).values()

        for item in comment_list:
            user_nid = item['user_info_id']
            user = models.UserInfo.objects.filter(nid=user_nid).values("username")[0]
            item['username'] = user['username']


        str_comment = commons.comment(comment_list)


        return HttpResponse(str_comment)


    elif req.method == "POST":
        username = req.session['user_info']['username']
        nid = req.session['user_info']['nid']
        print(nid)

        news_id = req.POST.get("news_id")
        reply_id = req.POST.get("reply_id")
        comment_content = req.POST.get("content")

        models.Comment.objects.create(
            content = comment_content,
            news_id = news_id,
            user_info_id = nid,
            parent_comment_id = reply_id,
        )


        com_obj = models.Comment.objects.last()
        # user_name = models.UserInfo.objects.filter(id=com_obj['user_info_id']).values('username')[0]


        response["status"] = True
        rp_dict = { 'news_id':com_obj.news_id,
                    'nid':com_obj.id,
                    'username':username,
                    'content':com_obj.content,
                    'ctime':com_obj.ctime,
                    'reply_id':reply_id}

        response["data"].update(rp_dict)

        return HttpResponse(json.dumps(response,cls=DataEncoder))


import datetime
class DataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self,obj)




def favor(req):
    response = {"status":True,"code":None,"message":""}

    if req.method == "POST":
        news_id = req.POST.get("news_id")
        nid = req.session['user_info']['nid']



        news_favor_count = models.News.objects.get(id=news_id)
        user_favor = news_favor_count.favor.filter(nid=nid).count()


        # print(news_favor_count.favor)
        # print(news_id)
        # print(nid)


        if not user_favor:
            news_favor_count.favor.add(nid)
            models.News.objects.filter(id=news_id).update(favor_count=F('favor_count')+1)
            response["code"] = 2301
            response["message"] = "获取点赞成功"
        else:
            news_favor_count.favor.remove(nid)
            models.News.objects.filter(id=news_id).update(favor_count=F('favor_count')-1)
            response["code"] = 2302
            response["message"] = "取消点赞成功"


        return HttpResponse(json.dumps(response))



def uploadImage(req):

    rep = {"status":False,"data":None}
    if req.method == "POST":
        up_img = req.FILES.get("img")

        print(up_img.name,up_img.size)

        import os
        file_path = os.path.join("statics","upload",up_img.name)

        f = open(file_path,'wb')
        for chunk in up_img.chunks():
            f.write(chunk)
        f.close()

        rep["status"] = True
        rep["data"] = file_path


    return HttpResponse(json.dumps(rep))



def conversion_func(empty_dict,dic):
    hr_lis = []
    zippend_lis = []
    stepby_num = len(dic)
    for item in empty_dict.items():
        hr_lis.append(item)

    val_lis = []
    key_lis = dic.keys()  # 获取转换字段的建和值

    for item_kv in hr_lis:
        val_lis.append(item_kv[1])

    num = len(val_lis)  # 计算出长度
    num_01 = num  # 设置一个固定的长度


    while True:
        for_count = int(num / stepby_num)
        if for_count != 0:  # 对列中的元素 进行切片操作
            num -= stepby_num
            start = num_01 - for_count * stepby_num
            end = num_01 - (for_count - 1) * stepby_num
            zippend = zip(key_lis, val_lis[start:end])

            zippend_lis.append(zippend)
        else:
            break

    return zippend_lis



def middle_func(labelname,empty_dict):
    full_dict ={}
    zippend_lis = []
    full_dict_lis = []
    # 测试设备配置
    equ_env = {
        "ser_type": "", "ser_mem": "", "ser_hard": "",
        "ser_cpu": "", "ser_soft": "",
        "cli_type": "", "cli_mem": "", "cli_hard": "",
        "cli_cpu": "", "cli_soft": ""
    }

    # 角色分配配置
    hr_dic = {
            "hr_task":"","hr_statime":"","hr_endtime":"",
            "dev_name":"","test_name":""
    }

    # 测试时间
    tt_con = {
        "phase":"","stime":"",
        "etime": "", "day": ""
    }

    # 测试阶段
    tac_des = {
        "label": "", "describe": ""
    }

    # 功能模块
    tac_from_con = {
        "func_label": "", "tag": ""
    }

    # 缺陷统计
    dev_bug = {
        "name": "", "num": ""
    }


    if labelname == '测试设备:':
        zippend = zip(equ_env.keys(), empty_dict.values())
        zippend_lis.append(zippend)

    elif labelname == '角色分配:':
        zippend_lis = conversion_func(empty_dict,hr_dic)

    elif labelname == '测试时间:':
        zippend_lis = conversion_func(empty_dict,tt_con)

    elif labelname == '测试阶段:':
        zippend_lis = conversion_func(empty_dict,tac_des)

    elif labelname == '功能模块:':
        zippend_lis = conversion_func(empty_dict,tac_from_con)

    elif labelname == '缺陷统计:':
        zippend_lis = conversion_func(empty_dict,dev_bug)



    for zippend_item in zippend_lis:
        for item in zippend_item:
            full_dict[item[0]] = item[1]
        full_dict_lis.append(full_dict.copy())


    return full_dict_lis



def modal_info(req):
    rep = BaseResponse()
    rep.status = True

    empty_dict = {}

    user_info = req.session['user_info']
    # print (user_info['nid'])
    u_nid = user_info['nid']

    modal_obj = models.ModalInfo.objects.get(user_info_id = u_nid)

    report_obj = models.ReportInfo.objects.get(user_info_id=u_nid)

    if req.method == "POST":
        req_post = req.POST

        for k,v in req_post.items():
            empty_dict[k] = v
        labelname=empty_dict.pop('label_name')


        if labelname == '测试设备:':
            modal_obj.equ_env=middle_func(labelname,empty_dict)


        elif labelname == '角色分配:':
            modal_obj.hr_lis = middle_func(labelname, empty_dict)


        elif labelname == '测试时间:':
            modal_obj.tt_con = middle_func(labelname,empty_dict)

        elif labelname == '测试阶段:':
            modal_obj.tac_des = middle_func(labelname,empty_dict)


        elif labelname == '功能模块:':
            modal_obj.tac_from_con = middle_func(labelname,empty_dict)
            modal_obj.func_lis = middle_func(labelname,empty_dict)


        elif labelname == '缺陷统计:':
            modal_obj.dev_bug = middle_func(labelname,empty_dict)
    modal_obj.save()

    if req.method == "GET":
        labelName = req.GET.get('labelName')
        labelValue = req.GET.get('labelValue')

        # print(labelName,labelValue)

        if labelName == '作者姓名:':
            report_obj.authorName = labelValue

        elif labelName == '覆盖范围:':
            report_obj.coverAge = labelValue
        elif labelName == '测试类型:':
            report_obj.testType = labelValue
        elif labelName == '方法说明:':
            report_obj.testStrategy = labelValue
        elif labelName == '背景介绍:':
            report_obj.backInfo = labelValue
        elif labelName == '参考文档:':
            report_obj.referenceFile = labelValue.split(" ")
        elif labelName == '风险说明:':
            report_obj.testRisk = labelValue
        elif labelName == '邮件内容:':
            report_obj.emailContent = labelValue
        elif labelName == '测试结论:':
            report_obj.testConclusion = labelValue
        elif labelName == '发送给@:':
            report_obj.emailList = labelValue
    report_obj.save()


    return HttpResponse(json.dumps(rep.__dict__))
    # return modal_info_dict


