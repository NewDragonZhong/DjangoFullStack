import json
from web import models
from backend.utils.spider_bugInfo import SpiderBugInfo



def spider_pro_info(username,password,nid):
    pass





def spider_bug_info(username,password,num,nid):
    '''
    爬取禅道上的BUG信息
    :param req:
    :return:
    '''
    # username = 'zhongxinlong'
    # password = 123456
    num = '035'
    login_url = r'http://it.bbdservice.com:8280/zentao/user-login.html'
    pro_url = r'http://it.bbdservice.com:8280/zentao/product-all-0-noclosed-order_desc-13-100-1.html'
    bug_url = r'http://it.bbdservice.com:8280/zentao/bug-browse-%s-0-all-0--598-500-1.html'

    sbi = SpiderBugInfo(username=username,password=password,num=num,login_url=login_url,pro_url=pro_url,bug_url=bug_url)

    pro_dict = json.dumps(sbi.product_info())

    bd = sbi.bug_info()
    bug_info_close = json.dumps(bd[0])
    bug_info_not_close = json.dumps(bd[1])

    data_dic = {"bug_info_close":bug_info_close,"bug_info_not_close":bug_info_not_close,"pro_info":pro_dict,"user_info_id":nid}

    ms = models.SpiderTable.objects.create(**data_dic)

    if ms == 'SpiderTable object':
        response = '数据获取成功！'
    else:
        response = '数据获取失败，请手动填写！'

    return response