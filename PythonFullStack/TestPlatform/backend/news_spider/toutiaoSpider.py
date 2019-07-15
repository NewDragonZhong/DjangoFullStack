# 头条爬虫
import requests
import json


class SpiderTouTiao:
    def __init__(self):
        # 总条目链接地址
        self.root_url = r'https://www.toutiao.com/api/pc/realtime_news/'
        # 分支条目链接地址
        self.branch_url = r'https://www.toutiao.com/a{0}'

    # 请求函数
    def req_func(self):
        realtime_news_req = requests.request(method='get',url=self.root_url)
        realtime_news_res = json.loads(realtime_news_req.text)
        return realtime_news_res


    # 今日头条_将总条目地址进行预处理函数
    def toutiao_precondition_func(self):
        realtime_news_res = self.req_func()
        for item in realtime_news_res["data"]:
            item["open_url"] = self.branch_url.format(item["group_id"])
        # 整理成可以入库的数据格式
        for item in realtime_news_res["data"]:
            item.setdefault("url", item.pop("open_url"))
            item.setdefault("img_href", item.pop("image_url"))
            item.setdefault("nt", 2)
            item.setdefault("user_id", 1)
            item.pop("group_id")
        return realtime_news_res["data"]




if __name__ == '__main__':
    stt = SpiderTouTiao()
    news_info = stt.toutiao_precondition_func()
    print(news_info)