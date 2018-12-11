import io,json,datetime
from django.shortcuts import HttpResponse,render,redirect


from web.forms.account import SendMsgForm,RegisterForm,LoginForm
from web import models

from backend.utils.response import BaseResponse
from backend.utils import check_code as CheckCode
from backend import commons
from backend.utils.message import email as send_email,email_report
from backend.utils.spider_bugInfo import SpiderBugInfo
from backend.utils.create_word import CreateWord
from backend.utils.mysql_bugInfo import MysqlBugInfo




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
    用户登录
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
    req.session.clear()
    return redirect('/index/')


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
            except Exception as e:
                print('报错信息:',e)
                rep.status = False
                rep.message = "爬取项目名称时，出错了！~"
        elif zentao_id == '2':
            try:
                pro_item_2 = mbi.product_info()
                models.SpiderProduct.objects.create(pro_info=pro_item_2)
                rep.status = True
                rep.data = pro_item_2
            except Exception as e:
                print('报错信息:', e)
                rep.status = False
                rep.message = "数据库连接时候时，出错了！~"

        else:
            rep.status = False
            rep.message = "没得你的项目信息！~"



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
                rep.message = '锅佬倌，点下拉框选项目！'
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
            rep.message = "没得你的BUG信息！~"


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
            rep.status = True
        except Exception as e:
            rep.status = False
            rep.message = e

    if req.method == "GET":
        print('这是文件的filePath:',filePath)

        obj_ri = models.ReportInfo.objects.get(user_info_id=u_nid)
        emailCount = obj_ri.emailContent
        email_list = cw.buffer_func(obj_ri.emailList)

        print('email_list:',email_list)
        print('email_list_type:', type(email_list))


        authorEmail = '%s@bbdservice.com' % u_name
        rep.message = "报告发送成功！"
        rep.status = True

        print('authorEmail:',authorEmail)
        print('ePassword:',ePassword)

        email_report(filePath, emailCount, email_list,authorEmail=authorEmail,ePassword=ePassword)




    return HttpResponse(json.dumps(rep.__dict__))