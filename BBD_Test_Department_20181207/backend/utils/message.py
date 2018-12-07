#!/usr/bin/env python
# -*- coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from email import encoders
from email.mime.base import MIMEBase
import os

def email(email_list,content,subject="BBD测试部-用户注册"):
    '''
    :param email_list: 要发送给的用户邮箱列表
    :param content: 输入的内容编码采用的utf-8格式
    :param subject: 邮件的主题
    :return: 就是发送一个通知邮件喏！~ 没啥好说的
    '''
    msg = MIMEText(content,'plain','utf-8')
    msg['From'] = formataddr(["BBD测试部",'17360137375@163.com'])
    msg['Subject'] = subject
    # SMTP服务
    server = smtplib.SMTP("smtp.163.com",25)
    server.login('17360137375@163.com','08123310190zxl')
    server.sendmail('17360137375@163.com',email_list,msg.as_string())
    server.quit()



def email_report(filePath,emailCount,email_list,ePassword,authorEmail='zhongxinlong@bbdservice.com'):
    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = formataddr(["BBD测试部",'zhongxinlong@bbdservice.com'])
    message['To'] = ','.join(email_list)
    subject = os.path.basename(filePath)
    message['Subject'] = subject

    # 填入正文
    message.attach(MIMEText(emailCount,'plain','utf-8'))

    with open(filePath, 'rb') as f:
        f_read = f.read()

    print('filePath:-----',filePath)
    # 构造附件文件
    # att1 = MIMEText(f_read,'base64','utf-8')
    # att1["Content-Type"] = 'application/octet-stream'
    # att1["Content-Disposition"] = 'attachment; filename="%s"' % subject
    # 合并构造体
    # message.attach(att1)

    # 添加附件
    ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    file = MIMEBase(maintype, subtype)
    file.set_payload(f_read)
    file.add_header('Content-Disposition', 'attachment', filename=subject)
    encoders.encode_base64(file)
    message.attach(file)



    try:
        server = smtplib.SMTP()
        server.connect('smtp.bbdservice.com')
        server.login(authorEmail, ePassword)
        server.sendmail(authorEmail, email_list, message.as_string())
        server.quit()
        print("邮件发送成功！")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件!")
