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


from random import randint, seed
import re
import time
import requests
import json

###### 全局变量 #####

sendkey = 'SCT64904TtD0qxfK3uR3nxUcDXMEYGoSF'   # 在 https://sct.ftqq.com/sendkey 中获取
openWechatPush = False      # 由于Server酱推送限制，免费用户只有5次推送次数，为了不浪费免费推送次数，测试调试请关闭微信推送服务
num = 1 # 默认每次注册的用户个数
passwd = 'wpq5201314'   # 每个注册账号默认的密码
qq_min = 10000000   # 注册的qq号最小值
qq_max = 2000000000 # 注册的qq号最大值(当qq号多次注册不成功时，修改范围有效)

####################


url_register = "https://cxkv2.xyz/auth/register"
url_login = "https://cxkv2.xyz/auth/login"
url_user = "https://cxkv2.xyz/user"
url_server = f"https://sctapi.ftqq.com/{sendkey}.send"
url_status = "https://sctapi.ftqq.com/push"

zh = []
token = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}

register_data = {
    'email':'',
    'name': '',
    'passwd': '',
    'repasswd': '',
    'wechat':   '',
    'imtype': 2,
    'code': 0,
    'geetest_challenge': 'c7e1249ffc03eb9ded908c236bd1996dc2',
    'geetest_validate': '2223223220167_3323322211079_22323332332231066dc',
    'geetest_seccode': '2223223220167_3323322211079_22323332332231066dc|jordan'
}

login_data = {
    'email': '',
    'passwd': '',
    'code': ''
}

mess = {
    'title': '我是标题',
    'desp': '我是内容'
}


# 获取随机账号
def getRandomZh():
    # 设计随机种子
    seed(time.time())
    qq_email = str(randint(qq_min, qq_max)) + "@qq.com"
    qq_password = passwd
    return qq_email, qq_password


# 注册账号
def register(qq_email, qq_password):
    print(f"email: {qq_email}\tpassword: {qq_password} ----", end="")
    register_data['email'] = qq_email
    register_data['name'] = qq_email
    register_data['wechat'] = qq_email
    register_data['passwd'] = qq_password
    register_data['repasswd'] = qq_password
    response = requests.post(url_register, headers=headers, data=register_data, timeout=6)
    if response.status_code != 200:
        print('恭喜你，机场已失效或你的IP被封了！')
        return
    elif json.loads(response.text)['ret'] != 1:
        print('注册失败！')
        time.sleep(2)
    else:
        print('注册成功！')
        if qq_email not in zh:
            zh.append(qq_email)
            login_data['email'] = qq_email
            login_data['passwd'] = qq_password
            login()
            time.sleep(1)


# 登录获取订阅
def login():
    try:
        response = requests.post(url_login, headers=headers, data=login_data)
        response = requests.get(url_user, headers=headers, cookies=response.cookies)
        tk = re.search(r'https:\/\/www.cxkv2.xyz\/link\/(.*?)\?mu=2', response.text).group()
        if tk not in token:
            token.append(tk)
    except Exception as e:
        print(f'错误：{e}')
    


# 向微信服务号推送消息
def sendMsg(url_status=None):
    mess['title'] = "新的V2ray订阅地址，请查收"
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
        randomZH = getRandomZh()
        register(randomZH[0], randomZH[1])
        num -= 1
    if zh:
        for tk in token:
            print(f'v2ray订阅：{tk}')
        if openWechatPush:
            sendMsg(url_status)
    # os.system('pause')
