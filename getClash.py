#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
                       _oo0oo_
                      o8888888o
                      88" . "88
                      (| -_- |)
                      0\  =  /0
                    ___/`---'\___
                  .' \\|     |// '.
                 / \\|||  :  |||// \
                / _||||| -:- |||||- \
               |   | \\\  - /// |   |
               | \_|  ''\---/''  |_/ |
               \  .-\__  '-'  ___/-. /
             ___'. .'  /--.--\  `. .'___
          ."" '<  `.___\_<|>_/___.' >' "".
         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
         \  \ `_.   \_ __\ /__ _/   .-` /  /
     =====`-.____`.___ \_____/___.-`___.-'=====
                       `=---='


     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

           佛祖保佑       永不宕机     永无BUG
'''

r'''
Author: @MGodmonkey
Date: 2021-08-14 17:26:42
LastEditTime: 2021-08-21 13:47:03
Description: 自动获取免费的clash订阅并自动推送到微信，免费期只有一天
FilePath: \lvglDemoc:\Users\17814\Desktop\getClash.py
'''


from random import randint, seed
import time
import requests
import json

###### 全局变量 #####

sendkey = 'SCT64904TtD0qxfK3uR3nxUcDXMEYGoSF'   # 在https://sct.ftqq.com/sendkey中获取
num = 2 # 每次获取的订阅数
passwd = 'wpq5201314'   # 每个注册账号默认的密码
qq_min = 10000000   # 注册的qq号最小值
qq_max = 2000000000 # 注册的qq号最大值(当qq号多次注册不成功时，修改范围有效)

####################


url_register = "https://feiniaoyun.tk/api/v1/passport/auth/register"
url_login = "https://feiniaoyun.tk/api/v1/passport/auth/login"
url_server = "https://sctapi.ftqq.com/SCT64904TtD0qxfK3uR3nxUcDXMEYGoSF.send"
url_status = "https://sctapi.ftqq.com/push"

zh = []
token = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}

data = {
    'email': '',
    'password': '',
    'invite_code': '',
    'email_code': ''
}

mess = {
    'title': '我是标题',
    'desp': '我是内容'
}


def getRandomZh():
    # 设计随机种子
    seed(time.time())
    qq_email = str(randint(qq_min, qq_max)) + "@qq.com"
    qq_password = passwd
    return qq_email, qq_password


# 注册账号
def register(qq_email, qq_password):
    print(f"email: {qq_email}\tpassword: {qq_password} ----", end="")
    data['email'] = qq_email
    data['password'] = qq_password
    response = requests.post(url_register, headers=headers, data=data, timeout=6)
    if response.status_code == 200:
        print('注册成功！')
        if qq_email not in zh:
            zh.append(qq_email)
        login()
        time.sleep(1)
    else:
        print("注册失败！")
        time.sleep(2)


# 登录获取token
def login():
    # browser = webdriver.Chrome()
    # browser.get("http://www.baidu.com")
    response = requests.post(url_login, headers=headers, data=data)
    if response.status_code == 200:
        tk = "https://feiniaoyun.tk/api/v1/client/subscribe?token=" + json.loads(response.text)['data']['token']
        if tk not in token:
            token.append(tk)


# 向微信服务号推送消息
def sendMsg(url_status=None):
    mess['title'] = "新的Clash订阅地址，请查收"
    desp = '';
    num = 0
    for i in zh:
        desp += f'## 账号: **{i}**\n\n> [{token[num]}]({token[num]})\n\n --- \n\n'
        num += 1

    mess['desp'] = desp
    response = requests.post(url_server, data=mess)
    if response.status_code == 200:
        localtime = time.strftime("%a %H:%M:%S [%y-%m-%d]", time.localtime())
        print(f'{localtime} ----消息发送成功！')
    # pushid = json.loads(response.text)['data']['pushid']
    # readkey = json.loads(response.text)['data']['readkey']
    # url_status += f'?id={pushid}&readkey={readkey}'
    # response = requests.get(url_status, headers=headers)
    # print(response.text)


if __name__ == '__main__':
    # num = int(input("请输入你要注册账号的数量："))
    while num:
        register(getRandomZh()[0], getRandomZh()[1])
        num -= 1
    if zh:
        for tk in token:
            print(tk)
        sendMsg(url_status)
    # os.system('pause')
