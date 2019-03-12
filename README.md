# 关于登录12306

### 说明
- 获取车票信息不是难点，而需要注意的是爬取粒度，太快可能招遭封ip，或者可以使用匿名ip做代理以及随机请求头池。
- 查询票不需要登录但购票需要，当在抢票时再登录很容易错过余票，故需要把登录放在抢票前。
- 登录12306的关键在于验证码认证，通过请求验证码地址和请求验证码检验地址来比对，
这里我走了弯路花了比较长时间，下面会说。


### 环境
    MacOS Mojave, python==3.6, scrapy, tkinter

### 解决验证码比对
- 验证码地址参数（get）:
   - login_site: E
   - module: login
   - rand: sjrand
   - 1552311782732: 
   - **callback: jQuery191021341557796491584_1552311770449**
   - _: 1552311770451

    时间都花在研究callback上了，一开始断定这个参数和提交验证验证码的地址时需要一致，却忘了callback实际只是不需要的参数。
    最后发现原来请求验证码url
    上面的可变参数都是不需要带的，只需要带上cookies和固定参数提交下面第二个url就可以了，之后再带上相同cookis去请求验证的地址。
    浏览器验证码请求地址：
    ```
    https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&1552311782732&callback=jQuery191021341557796491584_1552311770449&_=1552311770451
    ```
    实际请求地址
    ```
    https://kyfw.12306.cn/passport/captcha/captcha-image64？login_site=E&module=login&rand=sjrand
    ```

    - 接下来就比较顺利了
       1. 将验证码中正确图片坐标提交至:
       ```
       https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand
       ```
       2. 验证正确（返回json中"result_code": "4"）
       3. 将验证的设置的cookies加到之前cookie里去post请求下面登录地址，
       当然账户密码也是必须的，值得注意的是还需要带上之前的验证码坐标：
       ```
       https://kyfw.12306.cn/passport/web/login
       ```
       4. 还没完，获取上面登录set的cookis加到之前cookie中去请求获取token地址：
       ```
       https://kyfw.12306.cn/passport/web/auth/uamtk
       ```
       并获取返回json中token值以及新cookie继续加上...

       5. 带着cookie将token POST到验证地址:
       ```
       https://kyfw.12306.cn/otn/uamauthclient
       ```
       继续获取set-cookie加入原来的cookie中...

       6. 终于。。。完成登录了
       


### 关于验证码识别
- 涉及图像识别，建议网上购买对应接口
### 简单的登录界面
![avatar](https://github.com/DreamLay/Login12306/blob/master/imgs/login.png)
![avatar](https://github.com/DreamLay/Login12306/blob/master/imgs/after_login.png)