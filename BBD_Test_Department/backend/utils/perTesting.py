import gevent
import json
import requests
import time




class DataStatistics:
    def __init__(self,method,url,headers={},data={},count=1,flag=True):
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



    def url_req(self):
        # 任务开始时间
        self.startTime = time.clock()

        for i in range(self.num):
            self.response = requests.request(method=self.method,url=self.url,headers=self.headers,json=self.data,verify=self.flag)

            if self.response.status_code == 200 :
                # response_json = json.loads(response.text)
                self.req_success += 1
                # print('响应信息为：',response_json)
            else:
                print('响应的状态码：',self.response.status_code)
                self.req_lose += 1

        if self.response is None:
            self.req_lose += 1
            print('请求未发出！')
        self.endTime = time.clock()

        # 计算出每次请求消耗的时间
        self.countTime = self.endTime - self.startTime
        # 计算消耗的总时间
        self.totalTime +=  self.countTime

        self.data_list.append((self.req_success, self.req_lose,self.totalTime,self.countTime))


    def together_send(self):
        gevent.joinall([
            gevent.spawn(self.url_req),
        ])


    def data_response(self):

        return self.data_list.pop(-1)



if __name__ == '__main__':
    ds = DataStatistics(method='get',url='http://www.baidu.com',count=5)
    for i in range(5):
        ts = ds.together_send()
        print(ds.data_response())