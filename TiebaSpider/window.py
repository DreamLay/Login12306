import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk


class LoginWindow():

    def __init__(self):
        self.local = (
            "40,46","115,46","190,46","261,46",
            "43,120","117,120","190,120","253,120"
        )
        self.username = ''
        self.password = ''
        self.check = ''

    def init_sub(self):
        app = tk.Tk()
        app.title("登录12306")
        app.geometry("600x400")
        app.resizable(0,0)

        l_username = tk.Label(app,text="用户名: ")
        l_username.place(x=1,y=1,anchor='nw')
        t_username = tk.Entry(app)

        l_password = tk.Label(app,text="密码")
        t_password = tk.Entry(app)
        t_password['show'] = '*'

        l_username.place(x=80,y=30)
        t_username.place(x=140,y=30,width=120, height=25)
        # t_username.insert(0, '1234')
        l_password.place(x=300, y=30)
        t_password.place(x=360, y=30,width=120, height=25)
        # t_password.insert(0, '1234')

        im = Image.open('captcha.png')
        img = ImageTk.PhotoImage(im)
        l_img = tk.Label(app, image=img).place(x=150,y=80)

        lb_1 = tk.Label(app, text='①').place(x=155,y=125,width=10,height=11)
        lb_2 = tk.Label(app, text='②').place(x=232,y=125,width=10,height=11)
        lb_3 = tk.Label(app, text='③').place(x=303,y=125,width=10,height=11)
        lb_4 = tk.Label(app, text='④').place(x=375,y=125,width=10,height=11)
        lb_5 = tk.Label(app, text='⑤').place(x=155,y=197,width=10,height=11)
        lb_6 = tk.Label(app, text='⑥').place(x=232,y=197,width=10,height=11)
        lb_7 = tk.Label(app, text='⑦').place(x=303,y=197,width=10,height=11)
        lb_8 = tk.Label(app, text='⑧').place(x=375,y=197,width=10,height=11)

        t_check = tk.Entry(app)
        t_check.place(x=240,y=285,width=120, height=25)

        def getusername():
            username = t_username.get() #获取文本框内容
            password = t_password.get() #获取文本框内容
            check = ",".join([self.local[int(i)-1] for i in t_check.get()])
            # print(username, password, check)
            self.username = username
            self.password = password
            self.check = check
            if username.strip() == "" or password.strip() == "":
                username_warning = tk.Label(app,text="用户名和密码不能为空",fg='red')
                username_warning.place(x=1,y=1,anchor='nw')
            elif check.strip() == "":
                username_warning = tk.Label(app,text="验证码不能为空",fg='red')
                username_warning.place(x=1,y=1,anchor='nw')
            else:
                app.destroy()
        
        def quit():
            self.username, self.password, self.check = '000','000','quit'
            app.destroy()

        def refurbish():
            self.username, self.password, self.check = '000','000','s'
            app.destroy()
        
        def left_top_close():
            self.username, self.password, self.check = '000','000','quit'
            app.destroy()
        
        app.protocol("WM_DELETE_WINDOW", left_top_close)

        tk.Button(app,text="刷新",command=refurbish).place(x=386,y=85, width=60, height=25)
        tk.Button(app,text="确定",command=getusername).place(x=200,y=330, width=80, height=25)
        tk.Button(app,text="取消",command=quit).place(x=320,y=330, width=80, height=25)

        app.mainloop()

        return self.username, self.password, self.check


class UserInfoWindow():
    def __init__(self,username, name, id, phone_num):
        self.username = username
        self.name = name
        self.id = id
        self.phone_num = phone_num
        self.key = ''
        
    def init_sub(self):
        app = tk.Tk()
        app.title(self.name)
        app.geometry("600x300")
        app.resizable(0,0)

        frame = tk.Frame(app,width=500,height=250,bg='red')
        frame.pack()

        l_username = tk.Label(frame,text=self.username)
        l_username.pack()

        l_name = tk.Label(frame,text=self.name)
        l_name.pack()

        l_id = tk.Label(frame,text=self.id)
        l_id.pack()

        l_phone_num = tk.Label(frame,text=self.phone_num)
        l_phone_num.pack()

        cmb = ttk.Combobox(app)
        cmb.pack()
        cmb['value'] = ('上海','北京','天津','广州')
        
        def quit():
            self.key = 'quit'
            app.destroy()

        def refurbish():
            self.key = 's'
            app.destroy()
        
        def left_top_close():
            self.key = 'quit'
            app.destroy()
        
        app.protocol("WM_DELETE_WINDOW", left_top_close)

        tk.Button(app,text="刷新",command=refurbish).place(x=386,y=85, width=60, height=25)
        tk.Button(app,text="退出",command=quit).place(x=320,y=330, width=80, height=25)

        app.mainloop()
        return self.key



w = UserInfoWindow('1','2','3','4')
w.init_sub()