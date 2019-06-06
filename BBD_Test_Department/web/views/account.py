from backend.utils.perTesting import DataStatistics
import io,json,datetime
from django.shortcuts import HttpResponse,render,redirect
from django.db.models import F

from web.forms.account import SendMsgForm,RegisterForm,LoginForm
from web import models

from backend.utils.response import BaseResponse
from backend.utils import check_code as CheckCode
from backend import commons
from backend.utils.message import email as send_email,email_report
from backend.utils.spider_bugInfo import SpiderBugInfo
from backend.utils.create_word import CreateWord
from backend.utils.mysql_bugInfo import MysqlBugInfo


# ------------------- 基础功能 --------------------

def check_code(req):
    '''
    :param req:
    :return: 返回一个验证码
    '''
    stream = io.BytesIO()                           # 在内存中开辟一个区域用于存放图片 python3中用BytesIO()
    img,code = CheckCode.create_validate_code()     # 创建一张图片格式的字符串，将随机字符串code写到图片上
    img.save(stream,"PNG")                          # 规定好写进内存中的格式是什么
    req.session["CheckCode"] = code                 # 将字符串形式的验证码放到Session中
    return HttpResponse(stream.getvalue())



def send_msg(req):
    '''
    该功能主要用于注册时候发送，邮箱验证码
    :param req:
    :return:
    '''
    rep = BaseResponse()                                                        # 拿取接口需要返回的字段以及初始默认值
    form = SendMsgForm(req.POST)                                                # 拿取前端返回的数据进行邮箱校验
    if form.is_valid():
        _value_dict = form.clean()                                              # 如果信息正确输入，则拿取到正确的信息
        email = _value_dict['email']
        email_list = [email]

        has_exists_email = models.UserInfo.objects.filter(email=email).count()  # 如果有值则提示用户已经注册了
        if has_exists_email:
            rep.summary = "此邮箱号，已被注册！"
            return HttpResponse(json.dumps(rep.__dict__))
        current_date = datetime.datetime.now()                                  # 获取一个当前时间
        code = commons.random_code()                                            # 产生一个4位的随机验证码

        count = models.SendMsg.objects.filter(email=email).count()              # 统计发送了短信验证码的次数
        if not count:                                                           # 如果没有发送则发送，在表中记录
            models.SendMsg.objects.create(code=code,
                                          email=email,
                                          ctime=current_date)
            send_email(email_list,code)
            rep.status = True
        else:
            limit_day = current_date - datetime.timedelta(hours=1)              # 将创建时间减去一小时前的时间=一小时
            times = models.SendMsg.objects.filter(email=email,
                                                  ctime__gt=limit_day,  # 如果数据库中的时间大于 一小时前的时间(此时表明在1小时以内)
                                                  times__gt=9).count()  # 获取数据库中满足要求的数据(次数大于9)
            if times:
                rep.summary = "'已经超过发送的最大次数(请1小时后重试)'"
            else:
                unfreeze = models.SendMsg.objects.filter(email=email,
                                                         ctime__lt=limit_day).count()  # 获取一小时前的时间小于当前时间的数据(此时重置次数times)
                if unfreeze:
                    models.SendMsg.objects.filter(email=email).update(times=0)
                from django.db.models import F      # 导入F查询
                # 更新数据库中的数据
                models.SendMsg.objects.filter(email=email).update(code=code,
                                                                  ctime=current_date,
                                                                  times=F('times')+1)
                send_email(email_list, code)
                rep.status = True
    else:
        rep.summary = form.errors['email'][0]   # 如果不正确 则修改返回字段中的summary信息
    return HttpResponse(json.dumps(rep.__dict__))   # 返回时 把状态信息转换成json格式返回给前端



def register(req):
    '''
    注册
    :param req:
    :return:
    '''
    rep = BaseResponse()
    form = RegisterForm(req.POST)
    if form.is_valid():
        current_date = datetime.datetime.now()                      # 创建时间
        limit_day = current_date - datetime.timedelta(minutes=1)    # 一分钟
        _value_dict = form.clean()
        # 临时表中查询时间超过1分钟的数据
        is_valid_code = models.SendMsg.objects.filter(email=_value_dict['email'],
                                                      code=_value_dict['email_code'],
                                                      ctime__gt= limit_day).count()

        if not is_valid_code:
            rep.message['email_code'] = '验证码不正确或已经过期！'
            return HttpResponse(json.dumps(rep.__dict__))

        # 这里需要再一次的验证一下邮箱是否被注册
        has_exists_email = models.UserInfo.objects.filter(email=_value_dict['email']).count()

        if has_exists_email:
            rep.message['email'] = '邮箱已存在！'
            return HttpResponse(json.dumps(rep.__dict__))

        has_exists_username = models.UserInfo.objects.filter(username=_value_dict['username']).count()
        if has_exists_username:
            rep.message['email'] = '用户名已存在！'
            return HttpResponse(json.dumps(rep.__dict__))

        _value_dict['ctime'] = current_date
        _value_dict.pop('email_code')
        '''
            1.把得到的正确数据写入数据库
            2.获取当前用户的所有信息，以便注册成功后直接登录；
            3.删除临时表中无用的验证码数据；
        '''
        obj = models.UserInfo.objects.create(**_value_dict)
        user_info_dict = {'nid':obj.nid,'email':obj.email,'username':obj.username}
        models.SendMsg.objects.filter(email=_value_dict['email']).delete()

        req.session['is_login'] = True
        req.session['user_info'] = user_info_dict
        rep.status = True

    else:
        error_msg = form.errors.as_json()
        rep.message = json.loads(error_msg)
    return HttpResponse(json.dumps(rep.__dict__))



def login(req):
    '''
    用户登录 并且在登录后初始化各个表数据
    :param req:
    :return:
    '''

    rep = BaseResponse()
    form = LoginForm(req.POST)
    if form.is_valid():
        _value_dict = form.clean()
        # print(_value_dict)
        if _value_dict['code'].lower() != req.session['CheckCode'].lower():
            rep.message = {'code':[{'message':'验证码错误'}]}
            return HttpResponse(json.dumps(rep.__dict__))
        '''
        如果验证码正确，则进行Q查询
        '''
        from django.db.models import Q
        con = Q()
        q1 = Q()
        q2 = Q()

        q1.connector = 'AND'                # 在q1中创建逻辑关系符 ,然后把数据库中的值与用户输入的值进行比较
        q1.children.append(('email',_value_dict['user']))
        q1.children.append(('password',_value_dict['pwd']))


        q2.connector = 'AND'
        q2.children.append(('username',_value_dict['user']))
        q2.children.append(('password',_value_dict['pwd']))

        con.add(q1,'OR')
        con.add(q2,'OR')


        obj = models.UserInfo.objects.filter(con).first()

        if not obj:
            rep.message = {'user':[{'message':'用户名或邮箱或密码错误！'}]}
            return HttpResponse(json.dumps(rep.__dict__))

        req.session['is_login'] = True
        req.session['user_info'] = {'nid':obj.nid,'email':obj.email,'username':obj.username}

        rep.status = True

        # 查询 ModalInfo 数据库中 有没有该数据
        obj_mi = models.ModalInfo.objects.filter(user_info_id=obj.nid).first()
        if not obj_mi:
            models.ModalInfo.objects.create(user_info_id=obj.nid)

        # 查询 spidertable 数据中 有没有该数据
        obj_st = models.SpiderTable.objects.filter(user_info_id=obj.nid).first()
        if not obj_st:
            models.SpiderTable.objects.create(user_info_id=obj.nid)

        # 查询 reportInfo 数据中 有没有该数据
        obj_ri = models.ReportInfo.objects.filter(user_info_id=obj.nid).first()
        if not obj_ri:
            models.ReportInfo.objects.create(user_info_id=obj.nid)

        # 查询 pertestingtable 数据中 有没有该数据
        obj_ri = models.PertestingTable.objects.filter(user_info_id=obj.nid).first()
        if not obj_ri:
            models.PertestingTable.objects.create(user_info_id=obj.nid)

    else:
        error_msg = form.errors.as_json()
        rep.message = json.loads(error_msg)

    return HttpResponse(json.dumps(rep.__dict__))



def logout(req):
    '''
    用户注销
    :param req:
    :return:
    '''
    user_info = req.session['user_info']
    u_nid = user_info['nid']

    # 清除记录 性能测试表的数据
    models.PertestingTable.objects.get(user_info_id=u_nid).delete()

    req.session.clear()
    return redirect('/index/')



# ------------------- 新闻评论 --------------------

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






# ------------------- 报告发送 --------------------

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
            report_obj.emailList = labelValue.split(";")
    report_obj.save()


    return HttpResponse(json.dumps(rep.__dict__))
    # return modal_info_dict


def update_item(req):
    '''
    1. 初始化需要爬虫的准备数据
    2.更新项目 使用get请求 ，爬取项目相关数据 用post请求
    :param req:
    :return:
    '''
    rep = BaseResponse()


    # 旧禅道 爬虫信息初始化
    login_url = r'http://it.bbdservice.com:8280/zentao/user-login.html'
    pro_url = r'http://it.bbdservice.com:8280/zentao/product-all-0-noclosed-order_desc-13-100-1.html'
    bug_url = r'http://it.bbdservice.com:8280/zentao/bug-browse-%s-0-all-0--598-500-1.html'


    user_info = req.session['user_info']
    u_nid = user_info['nid']

    user_obj = models.UserInfo.objects.get(nid=u_nid)

    username = user_obj.username
    password = user_obj.password

    num = req.POST.get('itemId') # 获取用户选择的项目ID



    # 爬虫信息初始化
    ss = SpiderBugInfo(username, password, num, login_url, pro_url, bug_url)
    # 数据库信息初始化
    mbi = MysqlBugInfo(num)


    if req.method == 'GET':
        zentao_id = req.GET.get('zentao_id')  # 获取用户选择 禅道版本ID号
        print("zentao_id_get:", zentao_id)
        # 根据不同的 禅道版本选择 不同的方式获取项目信息
        if zentao_id == '1':
            try:
                pro_item_1 = ss.product_info()
                models.SpiderProduct.objects.create(pro_info=pro_item_1)
                rep.status = True
                rep.data = pro_item_1
                rep.message = "数据成功获取！"
            except Exception as e:
                print('报错信息:',e)
                rep.status = False
                rep.message = "爬取数据，出错！"
        elif zentao_id == '2':
            try:
                pro_item_2 = mbi.product_info()
                models.SpiderProduct.objects.create(pro_info=pro_item_2)
                rep.status = True
                rep.data = pro_item_2
                rep.message = "数据成功获取！"
            except Exception as e:
                print('报错信息:', e)
                rep.status = False
                rep.message = "远程数据库，拒绝访问！"

        else:
            rep.status = False
            rep.message = "无项目信息！~"



    if req.method == "POST":
        models_obj = models.SpiderTable.objects.get(user_info_id=u_nid)
        zentao_id = req.POST.get('zentao_id')  # 获取用户选择 禅道版本ID号
        print("zentao_id_post:", zentao_id)

        # 根据不同的 禅道版本选择 不同的方式获取BUG信息
        if zentao_id == '1':
            try:
                bug_lis,not_close = ss.bug_info()
                models_obj.bug_info_close = bug_lis
                models_obj.bug_info_not_close = not_close
                models_obj.save()

                rep.status = True
                rep.message = '数据爬取成功'
            except IndexError as e:
                print("报错信息:",e)
                rep.message = '请选择项目 或 该项目内容为空！'
                rep.status = False
        elif zentao_id == '2':
            try:
                bug_lis,not_close = mbi.bug_info()
                models_obj.bug_info_close = bug_lis
                models_obj.bug_info_not_close = not_close
                models_obj.save()

                rep.status = True
                rep.message = '数据爬取成功'
            except IndexError as e:
                print("报错信息:",e)
                rep.message = '锅佬倌，点下拉框选项目！'
                rep.status = False
        else:
            rep.status = False
            rep.message = "无BUG信息！~"


        # print("bug_lis",bug_lis)
        # print("not_close",not_close)
    return HttpResponse(json.dumps(rep.__dict__))



def creat_report(req):
    '''
    初始化变量
    :param req:
    :return:
    '''
    rep = BaseResponse()
    user_info = req.session['user_info']
    u_nid = user_info['nid']
    u_name = user_info['username']
    ePassword = models.UserInfo.objects.get(nid=u_nid).password
    headLine = req.POST.get('itemName')
    cw = CreateWord(u_nid, headLine)

    global filePath

    rep.status = True
    if req.method == "POST":
        try:
            filePath = cw.create_word() # 获取文档路径
            rep.message = "word生成成功！"
            rep.summary = "操作成功！"
            rep.status = True
        except Exception as e:
            rep.status = False
            rep.message = "word生成失败！"
            rep.summary = "操作失败！"
            print("报错原因：",e)


    if req.method == "GET":
        print('这是文件的filePath:',filePath)

        obj_ri = models.ReportInfo.objects.get(user_info_id=u_nid)
        emailCount = obj_ri.emailContent
        email_list = cw.buffer_func(obj_ri.emailList)

        # print('email_list:',email_list)
        # print('email_list_type:', type(email_list))


        authorEmail = '%s@bbdservice.com' % u_name
        rep.message = "报告发送成功！"
        rep.status = True

        # print('authorEmail:',authorEmail)
        # print('ePassword:',ePassword)

        email_report(filePath, emailCount, email_list,authorEmail=authorEmail,ePassword=ePassword)
    return HttpResponse(json.dumps(rep.__dict__))


from django.http import FileResponse # 导入下载传输模块
from django.utils.http import urlquote # 导入模块动态生成下载文件名
import os
import time

def report_download(req):
    time.sleep(2)
    fileName = os.path.basename(filePath) # 获取文件名字
    print(fileName)

    file = open(filePath,'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(urlquote(fileName))

    return response


# 自定义上传报告功能
def custom_file_upload(req):
    rep_cfu = BaseResponse()
    time.sleep(1)  # 让文件生成后再执行下载操作

    if req.method == 'POST':
        f = open(filePath, 'wb') #  打开即将要修改的文件
        try:
            file_obj = req.FILES.get('file')
            # print(file_obj,type(file_obj))  # 测试文件的类型
            for chunk in file_obj.chunks():
                f.write(chunk)
            rep_cfu.message = "修改文件上传成功！"
            rep_cfu.status = True
        except Exception as e:
            print("报错内容:",e)
            rep_cfu.message = "修改文件上传失败！"
            rep_cfu.status = False
        finally:
            f.close()

    return HttpResponse(json.dumps(rep_cfu.__dict__))




# ------------------- 性能测试 --------------------

def per_data_store(req):
    """
    获取前端传来的数据 后 存储
    :param req:
    :return:
    """
    user_info = req.session['user_info']
    u_nid = user_info['nid']

    # 拿取该表对象
    per_obj = models.PertestingTable.objects.get(user_info_id=u_nid)


    if req.method == 'POST':
        labelName = req.POST.get('labelName')
        labelValue = req.POST.get('labelValue')

        # 将从前端回去的值 逐一进行存储
        if labelName == 'reqMethods' and labelValue != '':
            per_obj.method = labelValue
        elif labelName == 'maxNum' and labelValue != '':
            per_obj.maxnum = labelValue
        elif labelName == 'onceNum' and labelValue != '':
            per_obj.oncenum = labelValue
        elif labelName == 'hosts' and labelValue != '':
            per_obj.hosts = labelValue
        elif labelName == 'paths':
            per_obj.paths = labelValue
        elif labelName == 'headers':
            per_obj.headers = labelValue
        elif labelName == 'datas':
            per_obj.datas = labelValue
        elif labelName == '_assert':
            per_obj.assert_dic = labelValue
        elif labelName == 'maxTime':
            per_obj.maxTime = labelValue
    per_obj.save()

    return HttpResponse("OK!")



def per_data_extract(req):
    """
    前端页面点击发送请求 后 执行的操作
    :param req:
    :return:
    """
    rep = BaseResponse()  # 创建 回调类对象
    user_info = req.session['user_info']  # 从session中拿取 用户ID
    u_nid = user_info['nid']

    # 拿取该表对象
    per_obj = models.PertestingTable.objects.get(user_info_id=u_nid)


    # 将部分数据进行处理 协议类型\并发数\请求头\请求体类型转换
    url = per_obj.hosts + per_obj.paths
    if not url.find('https'):
        flag = False
    else:
        flag =True

    # 查询到最大并发数 与 每次启动的并发数  并且进行计算
    maxNum = int(per_obj.maxnum)
    onceNum = int(per_obj.oncenum)
    if onceNum < maxNum:
        per_obj.oncenum += onceNum
    else:
        per_obj.oncenum = maxNum
    # print('此时的并发数为:',onceNum)

    # 请求头进行预处理
    try:
        headers = json.loads(per_obj.headers)

    except Exception:
        headers = {"Content-Type": "application/json"}

    # 请求体进行预处理
    try:
        datas = json.loads(per_obj.datas)
    except Exception:
        datas = ''

    # 请求断言进行预处理
    try:
        assert_dic = json.loads(per_obj.assert_dic)  # 对断言数据进行预处理
    except Exception:
        assert_dic = {}

    maxTime = per_obj.maxTime  # 接口响应的最大时间



    # 将表中的数据 初始化到 数据统计类中
    ds = DataStatistics(method=per_obj.method, url=url, headers=headers,
                        data=datas, count=onceNum,flag=flag,assert_dic=assert_dic,maxTime=maxTime)


    if req.method == 'POST':
        loop_num = req.POST.get('loop_num')     # 收集前端请求中的循环次数
        per_obj.loop_num += int(loop_num)       # 进行累加求值
        try:
            ds.together_send()      # 计算出来的指标
            rep.status = True
            data = ds.data_response() # 提取指标

            # 数据存储与计算
            per_obj.success_req += data[0]              # 成功请求数
            per_obj.lose_req += data[1]                 # 失败请求数
            per_obj.total_req += data[0] + data[1]      # 总请求数
            per_obj.total_time += data[2]               # 总共花销的时间
            per_obj.avg_time = per_obj.total_time / per_obj.loop_num  # 平均花销的时间

            # 以下数据 属于图表使用
            per_obj.count_time = data[3]     # 每次请求用时
            per_obj.rps= onceNum / data[3]   # 每次的并发数 / 每次请求用时
            # 保存数据入库
            per_obj.save()

            # 获取当前的系统时间
            lt = '{0}{1}:{2}:{3}'
            localtime = time.localtime()
            if localtime.tm_hour<12:
                lti = lt.format('上午',localtime.tm_hour,localtime.tm_min,localtime.tm_sec)
            elif 12<=localtime.tm_hour<14:
                lti = lt.format('中午', localtime.tm_hour, localtime.tm_min, localtime.tm_sec)
            else:
                lti = lt.format('下午', localtime.tm_hour, localtime.tm_min, localtime.tm_sec)


            # 将数据存入 前端回调类对象中(这里存在读写消耗)
            rep.data = [per_obj.success_req,per_obj.lose_req,per_obj.total_req,per_obj.avg_time,per_obj.total_time,per_obj.oncenum]
            rep.message = [per_obj.count_time,per_obj.rps,lti]
            # print(rep.data)
            rep.summary = '运行ing...'
        except (IndexError):
            rep.status = False
            rep.data = []
            rep.summary = '运行错误！接口请求失败。'


    return HttpResponse(json.dumps(rep.__dict__))



def per_data_clear(req):
    user_info = req.session['user_info']
    u_nid = user_info['nid']

    obj_data = models.PertestingTable.objects

    # 删除记录之后 再创建
    obj_data.get(user_info_id=u_nid).delete()

    obj_data.create(user_info_id=u_nid)

    return HttpResponse("OK!")