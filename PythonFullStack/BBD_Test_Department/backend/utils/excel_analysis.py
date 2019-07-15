import xlrd
import os


class ExcelAnalysis:
    def __init__(self):

        self.path1 = os.path.join(os.getcwd(), r'templates\TR_templates')
        self.souceFile_path = os.path.join(self.path1, 'template.xlsx')
        self._num = 0 # sheet 页面数


    # 返回模板下载地址
    def return_souceFile_path(self):
        return self.souceFile_path



    # 定义一个处理exc;e的函数 并且返回固定格式的内容存入数据库
    def modal_info_list(self,_dict,_num,_workbook):

        data_sheet = _workbook.sheets()[_num]
        # dataSheetName = data_sheet.name # 获取sheet名称
        rowNum = data_sheet.nrows  # sheet行数
        colNum = data_sheet.ncols  # sheet列数

        _list_headRow = []  # 盛放列表头的信息数据
        _list_result = []  # 盛放最后输出的信息数据
        _dict_zip = {}  # 盛放键值压缩的字典
        rows = data_sheet.row_values(0)  # 获取第一行的内容

        # 获取第一行的抬头 反应成对应的格式
        for item in rows:
            _list_headRow.append(_dict[item])

        for i in range(1, rowNum):
            _list_row = []
            for j in range(colNum):
                if data_sheet.cell(i, j).ctype == 3:  # 对日期格式进行转换 并 序列化添加
                    date_value = xlrd.xldate_as_tuple(data_sheet.cell_value(i, j),_workbook.datemode)
                    _list_row.append('%d/%d/%d' % (date_value[0:3]))
                else:
                    _list_row.append(data_sheet.cell_value(i, j))
            _list_zip = list(zip(_list_headRow, _list_row))
            for z in _list_zip:
                _dict_zip[z[0]] = z[1]
            _list_result.append(_dict_zip.copy())

        return _list_result


    # 定义一个函数存放列表头对应的字典 不需要输入 就是静态的执行文件
    def modal_dict(self):
        _dict_0 = {"服务器类型": "ser_type", "服务器内存": "ser_mem", "服务器硬盘": "ser_hard", "服务器CPU": "ser_cpu",
                   "服务器操作系统": "ser_soft",
                   "客户机类型": "cli_type", "客户机内存": "cli_mem", "客户机硬盘": "cli_hard", "客户机CPU": "cli_cpu",
                   "客户机操作系统": "cli_soft", }
        _dict_1 = {"任务名称": "hr_task", "开始时间": "hr_statime", "结束时间": "hr_endtime", "开发人员": "dev_name",
                   "测试人员": "test_name"}
        _dict_2 = {"测试阶段": "phase", "开始时间": "stime", "结束时间": "etime", "工作天数": "day", }
        _dict_3 = {"阶段名称": "label", "阶段描述": "describe"}
        _dict_4 = {"功能名称": "func_label", "是否通过": "tag"}
        _dict_5 = {"开发姓名": "name", "缺陷个数": "num"}

        return _dict_0, _dict_1, _dict_2, _dict_3, _dict_4, _dict_5


    # 定义一个确定modal_info_list函数参数的 方法
    def modal_param(self,_workbook):
        md_dict = self.modal_dict()  # 获取静态的字段名称
        web_modalinfo_table = {"equ_env": "", "hr_lis": "", "tt_con": "",
                               "tac_des": "", "tac_from_con": "", "dev_bug": ""}  # modal表中存放的字段比
        for item in web_modalinfo_table:
            web_modalinfo_table[item] = self.modal_info_list(md_dict[self._num], self._num,_workbook)
            self._num += 1
        return web_modalinfo_table