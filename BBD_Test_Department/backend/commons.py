#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import time
import hashlib
import collections
import json

def random_code():
    code=''
    for i in range(4):
        current = random.randrange(0,4)
        if current != i:
            temp = chr(random.randint(65,90))
        else:
            temp = random.randint(0,9)
        code += str(temp)
    return code


def generate_md5(value):
    r = str(time.time())
    obj = hashlib.md5(r.encode('utf-8'))
    obj.update(value.encode('utf-8'))
    return obj.hexdigest()


def tree_search(d_dic,commet_obj):
    # 在comment_dic中一个一个的寻找其回复的评论
    # 检查当前的评论的 reply_id 和 comment_dic中已有评论的nid 是否相同
    # 如果相同，则表示是回复的此信息
    # 如果不同，则需要去comment_dic 所有子元素中查找，如果一直未找中，则继续向下找
    for k,v_dic in d_dic.items():
        '''
        找回复的评论，将自己添加到其对应的字典中，
        例如：{评论一：{回复一：{},回复二：{}}}
        '''
        if k[0] == commet_obj[2]:
            d_dic[k][commet_obj] = collections.OrderedDict()
            return
        else:
            # 在当前第一个跟元素中递归的去寻找父级
            tree_search(d_dic[k],commet_obj)


def build_tree(comment_list):
    comment_dic = collections.OrderedDict
    for comment_obj in comment_list:
        if comment_obj[2] is None:
            # 如果是根评论，添加到comment_dic[评论对象] = {}
            comment_dic[comment_obj] = collections.OrderedDict()
        else:
            # 如果是回复评论，则需要在 comment_dic中找到其回复的评论
            tree_search(comment_dic,comment_obj)
    return comment_dic


def comment(comment_list):
    '''
     定义一个高效的获取评论层级和条数的方法
    :param comment_list:  数据库中的评论条数
    :return:   返回一个json格式的字符串
    '''
    comment_tree = []
    comment_list_dict = {}

    for row in comment_list:
        row.update({'children':[]})
        comment_list_dict[row['id']] = row


    for item in comment_list:
        parent_row = comment_list_dict.get(item['parent_comment_id'])
        if not parent_row:
            comment_tree.append(item)
        else:
            parent_row['children'].append(item)



    return json.dumps(comment_tree,cls=DataEncoder)



import datetime
class DataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self,obj)



if __name__ == '__main__':
    li_test = [{'id': 121, 'content': '第一条', 'user_info_id': 1, 'news_id': 1, 'parent_comment_id': None, 'device': None, 'ctime': datetime.datetime(2018, 6, 1, 6, 1, 16, 574500,)}, {'id': 122, 'content': '回复第一条', 'user_info_id': 1, 'news_id': 1, 'parent_comment_id': 1, 'device': None, 'ctime': None}]
    comment(li_test)
