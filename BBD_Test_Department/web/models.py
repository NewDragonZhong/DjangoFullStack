from django.db import models

# Create your models here.

class SendMsg(models.Model):
    nid = models.AutoField(primary_key=True)                    # 自定义主键,并且是个自增列
    code = models.CharField(max_length=6)
    email = models.CharField(max_length=32,db_index=True)       # 创建数据库索引
    times = models.IntegerField(default=0)                      # 设置默认值
    ctime = models.DateTimeField(auto_now_add=True)


class UserInfo(models.Model):
    nid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32,unique=True)      # 设置为唯一
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=32,unique=True)
    ctime = models.DateTimeField(auto_now_add=True)


# class NewsType(models.Model):
#     caption = models.CharField(max_length=16)


class News(models.Model):
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=128,null=True)
    url = models.URLField(null=True)
    ctime = models.DateTimeField(auto_now_add=True)  # 定义日期字段时选择让系统自动填写
    user = models.ForeignKey(to='UserInfo',to_field='nid',related_name='n',on_delete=models.CASCADE)     # 按照
    news_type_choices = [
        (1, "42区"),
        (2, "段子"),
        (3, "图片"),
        (4, "挨踢1024"),
        (5, "你问我答"),
    ]

    nt = models.IntegerField(choices=news_type_choices)

    # nt = models.ForeignKey(to='NewsType',to_field='id',related_name='tn')
    favor_count = models.IntegerField(default=0) # 点赞个数
    comment_count = models.IntegerField(default=0) #评论个数
    favor = models.ManyToManyField(to="UserInfo")



class Comment(models.Model):
    content = models.CharField(max_length=150)
    user_info = models.ForeignKey(to='UserInfo',to_field='nid',on_delete=models.CASCADE)
    news = models.ForeignKey('News',to_field='id',on_delete=models.CASCADE)
    parent_comment = models.ForeignKey("self",related_name='cp',null=True,on_delete=models.CASCADE)# 给自己进行评论，自关联
    device = models.CharField(max_length=16,null=True) # 使用的设备
    ctime = models.DateTimeField(auto_now_add=True)


class ModalInfo(models.Model):
    user_info = models.ForeignKey(to='UserInfo',to_field='nid',on_delete=models.CASCADE)
    # head_line = models.CharField(max_length=64)

    equ_env = models.CharField(max_length=64,null=True)
    hr_lis = models.CharField(max_length=128,null=True)
    tac_des = models.CharField(max_length=128,default='略')
    tac_from_con = models.CharField(max_length=128,null=True)
    dev_bug = models.CharField(max_length=128,null=True)
    tt_con = models.CharField(max_length=128,null=True)



class ReportInfo(models.Model):
    user_info = models.ForeignKey(to='UserInfo', to_field='nid', on_delete=models.CASCADE)
    authorName = models.CharField(max_length=32,null=True)
    coverAge = models.CharField(max_length=128, default='略')
    testType = models.TextField(default='略')
    testStrategy = models.CharField(max_length=128, default='略')
    backInfo = models.CharField(max_length=64,default='略')
    referenceFile = models.CharField(max_length=64, default='略')
    testRisk = models.CharField(max_length=64, default='略')
    testConclusion = models.CharField(max_length=128, default='略')
    emailContent = models.CharField(max_length=128, default='略')
    emailList = models.CharField(max_length=128, default='略')


class SpiderTable(models.Model):
    user_info = models.ForeignKey(to='UserInfo', to_field='nid',on_delete=models.CASCADE)
    bug_info_close = models.TextField(null=True,default='略')
    bug_info_not_close = models.TextField(null=True, default='略')


class SpiderProduct(models.Model):
    pro_info = models.CharField(max_length=64)



class PertestingTable(models.Model):
    user_info = models.ForeignKey(to='UserInfo', to_field='nid', on_delete=models.CASCADE)
    method = models.CharField(max_length=32,default='get')
    maxnum = models.IntegerField(max_length=16,default=10)      # 最大并发数
    oncenum = models.IntegerField(max_length=16, default=2)    # 每秒启动的并发数
    hosts = models.CharField(max_length=32,null=True)
    paths = models.CharField(max_length=64)
    headers = models.CharField(max_length=128)
    datas = models.CharField(max_length=128)

    success_req = models.IntegerField(max_length=16,default=0)
    lose_req = models.IntegerField(max_length=16,default=0)
    total_req = models.IntegerField(max_length=16,default=0)

    total_time = models.FloatField(max_length=16,default=0.0) # 请求总共花费的时间
    avg_time = models.FloatField(max_length=16,default=0.0)   #  请求的平均时间
    count_time = models.FloatField(max_length=16,default=0.0) # 单次并发请求的时间

    loop_num = models.IntegerField(max_length=16, default=0) # 请求循环次数
    rps = models.FloatField(max_length=16,default=0.0)  # 每秒处理的事务数

    assert_dic = models.CharField(max_length=128)  # 存储断言请求值
    maxTime = models.IntegerField(max_length=8, default=6)  # 存储允许的最大响应时间
    ctime = models.DateTimeField(auto_now_add=True)



class PertestingServersTable(models.Model):
    user_info = models.ForeignKey(to='UserInfo',to_field='nid',on_delete=models.CASCADE)
    # 服务器的登录信息
    server_add = models.CharField(max_length=32)
    server_port = models.IntegerField(max_length=16,default=22)
    server_username = models.CharField(max_length=32)
    server_password = models.CharField(max_length=32)
    # 记录服务的信息 --------**内存使用量**--------
    memory_used_per = models.CharField(max_length=16)  # 已经使用了的百分比
    # 记录服务的信息 --------**系统负债信息**--------
    sysLoad_time = models.CharField(max_length=16)  # 当前的服务器时间
    sysLoad_runTime = models.CharField(max_length=16)  # 当前服务器的运行时长
    sysLoad_userNum = models.CharField(max_length=16)  # 当前用户数
    sysLoad_loadLevel_1min = models.CharField(max_length=16)  # 当前的负债均衡情况(分别取1min,5min,15min的均值)
    sysLoad_loadLevel_5min = models.CharField(max_length=16)  # 当前的负债均衡情况(分别取1min,5min,15min的均值)
    sysLoad_loadLevel_15min = models.CharField(max_length=16)  # 当前的负债均衡情况(分别取1min,5min,15min的均值)


class UserFilesPaths(models.Model):
    user_info = models.ForeignKey(to='UserInfo',to_field='nid',on_delete=models.CASCADE)
    word_souceFile_path = models.CharField(max_length=32)
    word_resultFile_path = models.CharField(max_length=32)
    excel_souceFile_path = models.CharField(max_length=32)