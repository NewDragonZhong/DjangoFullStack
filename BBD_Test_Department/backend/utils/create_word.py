from docxtpl import DocxTemplate,RichText,InlineImage
from docx.shared import Mm, Inches, Pt
import json
from web import models
import os
import time



class CreateWord:
    def __init__(self,nid,headLine):
        self.obj_ri = models.ReportInfo.objects.get(user_info_id = nid)
        self.obj_sp = models.SpiderTable.objects.get(user_info_id=nid)
        self.obj_mi = models.ModalInfo.objects.get(user_info_id=nid)

        self.headLine = headLine

        self.path1 = os.path.join(os.getcwd(), r'templates\TR_templates')
        self.path2 = r'C:\Users\Administrator\Desktop\%s' % nid
        self.souceFile_path = os.path.join(self.path1, 'test_pro2.docx')
        self.resultFile_path = os.path.join(self.path2, r'%s测试报告.docx' % self.headLine)

        # print(self.obj_mi.equ_env)
        # print(type(self.obj_mi.equ_env))
        # print(json.loads(json.dumps(eval(self.obj_mi.equ_env))))
        # print("--------******--------")
        # print(type(json.loads(json.dumps(eval(self.obj_mi.equ_env)))))

    def return_fileName(self):
        return self.resultFile_path


    def buffer_func(self,data):
        result = json.loads(data.replace('"',' ').replace("'",'"'))
        # print('result:',result)
        return result



    def create_word(self):
        self.tpl = DocxTemplate(self.souceFile_path)

        # 创建文件夹目录
        try:
            os.makedirs(self.path2)
        except FileExistsError as e:
            print("目录已经存在，请继续")
        finally:
            print(self.resultFile_path)


        self.context = {
            "headLine": self.headLine,
            "authorName": self.obj_ri.authorName,
            "ctime": time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
            "testType":self.obj_ri.testType,
            "testStrategy":self.obj_ri.testStrategy,
            "coverAge":self.obj_ri.coverAge,
            "backInfo":self.obj_ri.backInfo,
            "emailContent":self.obj_ri.emailContent,
            "referenceFile":self.buffer_func(self.obj_ri.referenceFile),
            "testRisk":self.obj_ri.testRisk,
            "testConclusion":self.obj_ri.testConclusion,

            "bug_info_close":self.buffer_func(self.obj_sp.bug_info_close),
            "bug_info_not_close": self.buffer_func(self.obj_sp.bug_info_not_close),

            "equ_env": self.buffer_func(self.obj_mi.equ_env),
            "hr_lis": self.buffer_func(self.obj_mi.hr_lis),
            "tt_con": self.buffer_func(self.obj_mi.tt_con),
            "tac_des": self.buffer_func(self.obj_mi.tac_des),
            "tac_from_con": self.buffer_func(self.obj_mi.tac_from_con),
            "dev_bug": self.buffer_func(self.obj_mi.dev_bug),

        }

        self.tpl.render(self.context)

        self.tpl.save(self.resultFile_path)

        return self.resultFile_path




# def word_test():
#
#     path1 = os.path.join(os.getcwd(),r'templates\TR_templates')
#     template_file_name = 'test_pro2.docx'
#     result_file_name = 'result_pro.doxc'
#
#     soucFile_path = os.path.join(path1,template_file_name)
#     resultFile_path = os.path.join(path1,result_file_name)
#
#
#     return path1


# def zxl_word():
#     tt_con = [{"phase": "指标测试", "stime": "2018-10-10", "etime": "2018-10-20", "day": "10"},{"phase": "系统测试", "stime": "2018-10-11", "etime": "2018-10-16", "day": "5"}]
#
#     tac_descr = '''
#                 功能性测试用例主要采用边界值法、等价类划分、判定表、错误类推等测试方法进行用例设计。
#                 并从以下几个方面对功能进行测试：
#                 基础功能实现是否正常、功能拓展（隐含的当正确实现的功能是否正确实现）、
#                 稳健性（容错、异常操作、错误数据等系统是否处理正确）、
#                 模块关联性（各个模块之间的约束控制数据流转是否正确，是否影响到该模块的正确使用）、界面友好性（界面设计是否符合用户需求，术语展示是否标准用词是否恰当等）等等
#             '''
#
#     obj_word = models.ReportTemplate.objects.filter(id=1)
#
#
#     context = {
#         "headline" : obj_word[0].head_line,
#         "author" : obj_word[0].author,
#         "ctime" : obj_word[0].ctime,
#         "back_info" : obj_word[0].back_info,
#         "func_lis" : obj_word[0].func_lis,
#         "scope" : obj_word[0].scope,
#         "doc_lis" : obj_word[0].doc_lis,
#         "tac_descr":tac_descr,
#         "env_img" : obj_word[0].env_img,
#         "equ_env" : json.loads(obj_word[0].equ_env),
#         "tt_con":tt_con,
#         "hr_lis" : json.loads(obj_word[0].hr_lis),
#         "tac_des" : json.loads(obj_word[0].tac_des),
#         "tac_from_con" : json.loads(obj_word[0].tac_from_con),
#         "test_type" : obj_word[0].test_type,
#         "bug_info" : obj_word[0].bug_info,
#     }
#
#     tpl.render(context)
#
#     # return tpl.save(r'F:\test\FrontSystem_web-master\chouti\templates\TR_templates\test2.docx')


if __name__ == '__main__':
    wt = word_test()
    print (wt)

