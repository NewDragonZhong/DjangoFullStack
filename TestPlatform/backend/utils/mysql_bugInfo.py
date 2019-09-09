import pymysql as ps



class MysqlBugInfo:
    def __init__(self,pro_id):
        # self.db = ps.connect(host='127.0.0.1',port=7575,user="root",passwd="123456",db='zentao',charset='utf8')

        # 初始化项目库 参数信息
        self.sqlP = '''
                    SELECT id,name FROM zt_product
                    '''
        self.result_p = {}  # {'pro_name':'pro_id',.....}

        # 初始化项目BUG 参数信息
        self.sqlB = '''
                SELECT id,title,status,severity FROM zt_bug WHERE product = %s;
            ''' %(pro_id)
        self.result_b ={
            "id": "",
            "title": "",
            "status": "",
            "level": "",
            "sum": "",
        }


    def product_info(self):
        db = ps.connect(host='10.28.200.161', port=3306, user="zentao", passwd="123456", db='zentao', charset='utf8')
        cursor_p = db.cursor()  # 获取操作游标
        cursor_p.execute(self.sqlP) # 执行sql语句

        result =  cursor_p.fetchall()

        for item in result:
            self.result_p[item[1]] = item[0]
        db.close()

        return self.result_p



    def bug_info(self):
        db = ps.connect(host='10.28.200.161', port=3306, user="zentao", passwd="123456", db='zentao', charset='utf8')
        cursor_p = db.cursor()  # 获取操作游标
        cursor_p.execute(self.sqlB)  # 执行sql语句

        bug_lis = [] # 指定一个存放BUG 信息的列表

        result = cursor_p.fetchall()

        for item in result:
            self.result_b["id"] = item[0]
            self.result_b["title"] = item[1]
            self.result_b["status"] = item[2]
            self.result_b["level"] = item[3]
            self.result_b["sum"] = len(result)

            bug_lis.append(self.result_b.copy())
            # self.result_b = {"id": "", "title": "", "status": "", "level": "", "sum": ""}


        # 定义关闭的BUG 和未关闭的BUG
        close_num = 0
        nonclose_num = 0
        not_close = []
        for item in bug_lis:
            if item['status'] != 'closed':
                nonclose_num += 1
                not_close.append(item)
            else:
                close_num +=1

        bug_lis[0]["close_num"] = close_num
        bug_lis[0]["nonclose_num"] = nonclose_num


        db.close()

        return bug_lis,not_close




if __name__ == '__main__':
    mb = MysqlBugInfo()
    # print(mb.product_info())
    print(mb.bug_info()[0])
    print("-----------------------****************---------------------------")
    print(mb.bug_info()[1])