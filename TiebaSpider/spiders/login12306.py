# -*- coding: utf-8 -*-
import tkinter as tk
import scrapy
import base64
import time
import json
import re
from urllib import parse
from TiebaSpider.window import LoginWindow, UserInfoWindow


class Login12306Spider(scrapy.Spider):
    name = 'login12306'
    # allowed_domains = ['kyfw.12306.cn']
    start_urls = ['https://kyfw.12306.cn/otn/resources/login.html']
    headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Referer": "https://kyfw.12306.cn/otn/view/index.html",

        }
    cookie = dict()
 
    def start_requests(self):
        yield scrapy.Request(
            'https://kyfw.12306.cn/otn/login/conf',
            callback=self.get_captcha
        )


    def get_captcha(self, response):
        new_cookies = self.get_ck(response)
        yield scrapy.Request(
            'https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand',
            cookies=self.cookie,
            callback=self.check,
            dont_filter = True
        )

    def get_image(self, response):
        
        res = response.body.decode()
        image_base64 = ''
        try:
            image_base64 = json.loads(res)['image']
        except:
            image_base64 = response.xpath("//image/text()").extract_first()

        image = base64.b64decode(image_base64)
        with open('captcha.png', 'wb') as f:
            f.write(image)


    def check(self, response):

        new_cookies = self.get_ck(response)
        self.get_image(response)
        window = LoginWindow()
        username, password, answer = window.init_sub()
        print(username, password, answer)
        if answer == 's':
            yield scrapy.Request(
            'https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand',
            cookies=self.cookie,
            callback=self.check,
            dont_filter = True)
        elif answer == 'quit':
            pass
        else:
            answer_code = parse.quote_plus(answer)
            yield scrapy.FormRequest(
                'https://kyfw.12306.cn/passport/captcha/captcha-check',
                cookies=self.cookie,
                callback=self.logging,
                formdata=dict(
                    answer=answer,
                    login_site='E',
                    rand='sjrand'
                ),
                meta={"username":username,"password":password,"answer":answer},
                dont_filter = True
            )

    def logging(self, response):

        new_cookies = self.get_ck(response)
        answer,username,password = response.meta["answer"],response.meta["username"],response.meta["password"]
        result_code = response.xpath("//result_code/text()").extract_first()

        if not result_code:
            res = response.body.decode()
            result_code = json.loads(res)['result_code']
        
        if int(result_code) == 4:

            yield scrapy.FormRequest(
                'https://kyfw.12306.cn/passport/web/login',
                formdata=dict(
                    username=username,
                    password=password,
                    appid='otn',
                    answer=answer
                ),
                cookies=self.cookie,
                callback=self.get_token,
                dont_filter = True
            )
        else:
            print("验证码校验失败，请重新验证...")
            time.sleep(3)
            yield scrapy.Request(
            'https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand',
            cookies=self.cookie,
            callback=self.check,
            dont_filter = True,
            meta=response.meta)


    def get_token(self, response):
        new_cookies = self.get_ck(response)
        yield scrapy.FormRequest(
            'https://kyfw.12306.cn/passport/web/auth/uamtk',
            cookies=self.cookie,
            formdata={"appid":"otn"},
            callback=self.get_auth,
            dont_filter = True)


    def get_auth(self, response):
        new_cookies = self.get_ck(response)
        res = json.loads(response.body.decode())
        yield scrapy.FormRequest(
            'https://kyfw.12306.cn/otn/uamauthclient',
            cookies=self.cookie,
            formdata={"tk":res['newapptk']},
            callback=self.after_login,
            dont_filter = True)


    def after_login(self, response):
        result_code = json.loads(response.body.decode())['result_code']
        if int(result_code) == 0:
            print('登录成功成功！')
            new_cookies = self.get_ck(response)
            yield scrapy.Request(
                'https://kyfw.12306.cn/otn/modifyUser/initQueryUserInfoApi',
                # method='POST',
                cookies=self.cookie,
                callback=self.parse,
                dont_filter = True
            )
        else:
            print("获取token失败")
            yield scrapy.Request(
            'https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand',
            cookies=self.cookie,
            callback=self.check,
            dont_filter = True
            )


    def parse(self, response):
        person_info = json.loads(response.body.decode())['data']['userDTO']['loginUserDTO']
        username = person_info['user_name']
        name = person_info['name']
        id = person_info['id_no']
        phone_num = person_info['agent_contact']
        uswd = UserInfoWindow(username,name,id,phone_num)
        key = uswd.init_sub()
        if key == 's':
            yield scrapy.Request(
                'https://kyfw.12306.cn/otn/modifyUser/initQueryUserInfoApi',
                # method='POST',
                cookies=self.cookie,
                callback=self.parse,
                dont_filter = True
            )
    
        elif key == 'quit':
            pass
        
        else:
            yield scrapy.Request()

    def get_ck(self,response):
        set_cookies = response.headers.getlist('set-Cookie')
        set_cookie = { i.decode().split(';')[0].split('=')[0]: i.decode().split(';')[0].split('=')[1] for i in set_cookies}
        for key in set_cookie:
            if set_cookie[key] != "":
                self.cookie[key] = set_cookie[key]
        # print(self.cookie)
        return set_cookie

