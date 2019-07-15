import requests
from lxml import etree


class SpiderBugInfo:
    def __init__(self,username,password,num,login_url,pro_url,bug_url):
        self.login_tag = requests.Session()
        self.login_tag.auth = (username,password)
        self.login_tag.get(login_url)

        # 定义一个资源函数 存放请求信息
        # 返回 一个列表 和字典
        self.pro_url = pro_url
        self.pro_path = r'//tbody[@id="productTableList"]//a'

        self.bug_url = bug_url % (num)
        self.bug_path_1 = r'//table[@id="bugList"]//tr[@class="text-center"]//a'  # 抓取到ID 和 BUG标题
        self.bug_path_2 = r'//table[@id="bugList"]//tr[@class="text-center"]//td[5]'  # 抓取状态
        self.bug_path_3 = r'//table[@id="bugList"]//tr[@class="text-center"]//td[2]/span'  # 抓取严重程度




    # 定义一个清洗函数 获取禅道首页信息
    # 形式如：{'pro_name':'pro_num',.....}
    def dq_info(self,url,path):
        res = self.login_tag.get(url)
        pro_html = etree.HTML(res.text)
        infos = pro_html.xpath(path)
        data = []

        for info in infos:
            data.append(info.text)
        return data


    def product_info(self):
        data = self.dq_info(self.pro_url,self.pro_path)
        dic = {}

        for i in range(len(data) - 1):
            if i % 2 == 0:
                dic[data[i + 1]] = data[i]
        return dic


    def bug_info(self):
        dic = {
            "id": "",
            "title": "",
            "status": "",
            "level": "",
            "sum": "",
        }
        bug_lis = []
        df1 = list(filter(None, self.dq_info(self.bug_url,self.bug_path_1)))
        df2 = self.dq_info(self.bug_url,self.bug_path_2)
        df3 = self.dq_info(self.bug_url,self.bug_path_3)


        i = 1
        while i < len(df1):
            if i % 2 != 0:
                dic["id"] = df1[i - 1]
                dic["title"] = df1[i]
                bug_lis.append(dic)
            i += 1
            dic = {"id": "", "title": "", "status": "", "level": "", "sum": ""}

        n = 1
        for item in bug_lis:
            item["status"] = df2[n - 1]
            item["level"] = df3[n - 1]
            item["sum"] = len(df2)
            n += 1

        close_num = 0
        nonclose_num = 0
        not_close = []
        for item in bug_lis:
            if item["status"] == "已关闭":
                close_num += 1
            else:
                nonclose_num += 1
                not_close.append(item)

        bug_lis[0]["close_num"] = close_num
        bug_lis[0]["nonclose_num"] = nonclose_num

        return bug_lis, not_close



if __name__ == '__main__':
    login_url = r'http://it.bbdservice.com:8280/zentao/user-login.html'
    pro_url = r'http://it.bbdservice.com:8280/zentao/product-all-0-noclosed-order_desc-13-100-1.html'
    bug_url = r'http://it.bbdservice.com:8280/zentao/bug-browse-%s-0-all-0--598-500-1.html'

    username = 'zhongxinlong'
    password = 123456
    num = '035'
    ss =SpiderBugInfo(username,password,num)