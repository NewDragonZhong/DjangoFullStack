#  把脚本加入到项目中
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "change_chouti.settings")
django.setup()
# ------***------
from web import models
from backend.news_spider.toutiaoSpider import SpiderTouTiao





# 今日头条入库函数
def toutiao():
    # 数据库表对象
    news_toutiao = models.News.objects
    # 解析后的返回值
    spider_toutiao = SpiderTouTiao()
    news_info = spider_toutiao.toutiao_precondition_func()

    try:
        for item in news_info:
            news_toutiao.create(**item)
            message = "Finish,OK!~~"
    except Exception as e:
            message = "Error,NO!~~"


    return message



if __name__ == '__main__':
    print(toutiao())