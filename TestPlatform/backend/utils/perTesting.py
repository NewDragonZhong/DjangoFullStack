import gevent
import json
import requests
import time




class DataStatistics:
    def __init__(self,method,url,headers={},data={},count=1,flag=True,assert_dic={},maxTime=6):
        self.method = method
        self.url = url
        self.headers = headers
        self.data = data
        self.num = count
        self.data_list = []
        self.response = ''
        # 成功发送的请求数 和 失败的请求数
        self.req_success = 0
        self.req_lose = 0
        self.startTime = 0
        self.endTime = 0
        self.countTime = 0
        self.totalTime = 0
        self.flag = flag
        self.assert_dic = assert_dic
        self.logic_include = False  # 逻辑开关 包含的字符
        self.logic_outclude = False # 逻辑开关 不包含的字符
        self.maxTime = maxTime


    # 请求发送 以及 判断的主方法
    def url_req(self):
        self.startTime = time.clock() # 任务开始时间

        for i in range(self.num):
            self.response = requests.request(method=self.method,url=self.url,headers=self.headers,json=self.data,verify=self.flag)

            if self.assert_dic == {}:   # 判断用户 是否使用了 控制断言
                if self.response.status_code == 200:
                    self.req_success += 1
                else:
                    print('响应的状态码：', self.response.status_code)
                    self.req_lose += 1
            else:
                self.response.encoding = 'utf-8'  # 设置返回体的编码格式 默认为utf-8
                try:
                    self.logic_include = self.assert_dic['include'] in self.response.text
                    self.logic_outclude = self.assert_dic['outclude'] not in self.response.text
                except KeyError as e:
                    print('输入的键不存在！')
                finally:
                    if self.response.status_code == 200 and self.logic_include or self.logic_outclude :
                        self.req_success += 1
                    else:
                        print('响应的状态码：',self.response.status_code)
                        self.req_lose += 1

        if self.response is None:
            self.req_lose += 1
            print('请求未发出！')
        self.endTime = time.clock()

        # 计算出每次请求消耗的时间
        self.countTime = self.endTime - self.startTime
        # 如果响应的时效大于用户设置的时效则 认为请求失败
        if self.countTime > self.maxTime:
            self.req_success -= self.num
            self.req_lose += self.num

        # 计算消耗的总时间
        self.totalTime +=  self.countTime

        self.data_list.append((self.req_success, self.req_lose,self.totalTime,self.countTime))

    # 协程发送方法
    def together_send(self):
        gevent.joinall([
            gevent.spawn(self.url_req),
        ])

    # 取数方法
    def data_response(self):

        return self.data_list.pop(-1)



if __name__ == '__main__':
    ds = DataStatistics(method='get',url='http://www.baidu.com',count=5)
    for i in range(5):
        ts = ds.together_send()
        print(ds.data_response())