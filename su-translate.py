from tkinter import *
import tkinter.messagebox as mbox
import json
import time
import hashlib
import threading
import base64
import uuid

import requests
import win32gui
import win32con
from PIL import ImageGrab


APP_KEY = 'XXX.....'      # please write YOUR APP_key FROM YOUDAO_API
APP_SECRET = 'XXXX.....'  # please write YOUR APP_SECRET FROM YOUDAO_API


def jietu():
    app01.deiconify()
    hd = win32gui.FindWindow(0, "picture")  # 根据标题找到窗口句柄
    win32gui.ShowWindow(hd, 1)  # 把句柄传给showwindow实现显示隐藏效果 1为显示
    app01.attributes("-topmost", True)
    app01.attributes("-fullscreen", True)
    app01.attributes("-alpha", 0.5)
    # bmpinfo = [0, 0]
    canvas01 = Canvas(app01, width=2160, height=1440, bg="gray")
    ans = Label(app01, font=("JetBrains Mono", 10))
    app01.bind('<Button-1>', xFunc1)  # 绑定鼠标左键点击事件
    app01.bind('<B1-Motion>', lambda event: xFunc2(event, canvas01, ans))  # 绑定鼠标左键点击移动事件
    app01.bind('<ButtonRelease-1>', lambda event: xFunc01(event, canvas01, ans))  # 绑定鼠标左键点击释放事件
    app01.bind('<Escape>', lambda event: xfunc_out(event, ans))  # 绑定Esc按键退出事件
    return


def xfunc_out(event, ans):
    app01.attributes("-topmost", 0)
    app01.attributes("-fullscreen", 0)
    app01.attributes("-alpha", 1)
    ans.destroy()
    hd = win32gui.FindWindow(0, "picture")  # 根据标题找到窗口句柄
    win32gui.ShowWindow(hd, 0)  # 把句柄传给showwindow实现显示隐藏
    # app01.iconify()


def xFunc1(event):
    print(event.state)
    global bmpinfo
    bmpinfo = [event.x, event.y]


def xFunc01(event, canvas01, ans):
    print(event.state)

    if event.x == bmpinfo[0] or event.y == bmpinfo[1]:
        # mem_dc.DeleteDC()
        # win32gui.DeleteObject(screenshot.GetHandle())
        return
    else:
        app01.attributes("-alpha", 0)
        im = ImageGrab.grab((bmpinfo[0]*1.5, bmpinfo[1]*1.5, event.x*1.5, event.y*1.5))
        print(f"此时左上角和右下角为：{bmpinfo[0]}, {bmpinfo[1]}, {event.x}, {event.y}")
        imgName = 'tmp.png'
        canvas01.destroy()
        im.save(imgName)
        app01.attributes("-alpha", 1)
        app01.attributes("-fullscreen", 0)
        app01.geometry("%dx%d+%d+%d" % (event.x-bmpinfo[0], event.y-bmpinfo[1], bmpinfo[0], bmpinfo[1]))
        # mem_dc.DeleteDC()
        # win32gui.DeleteObject(screenshot.GetHandle())
        req = run()
        if req['errorCode'] == '0':
            line_num = len(req['resRegions'])
            tex = ''
            for i in range(0, line_num):
                tex = tex+req['resRegions'][i]['tranContent']+'\n'
            ans['text'] = tex
            ans['wraplength'] = event.x-bmpinfo[0]
            ans['justify'] = "center"
            ans['fg'] = 'black'
            ans.grid(row=0, column=0)


def encrypt(signStr):
    hash_algorithm = hashlib.md5()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def encrypt01(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def run():
    uuid01 = str(uuid.uuid1())
    pig = open(r'tmp.png', 'rb')  # 二进制方式打开图文件
    pig1 = base64.b64encode(pig.read()).decode('utf-8')  # 读取文件内容，转换为base64编码
    pig.close()
    url3 = 'https://openapi.youdao.com/ocrtransapi'
    signStr = APP_KEY + pig1 + uuid01 + APP_SECRET
    head3 = {'Content-type':'application/x-www-form-urlencoded; charset=UTF-8'}
    data3 = {
        'type': '1',
        'from': 'auto',
        'to': 'zh-CHS',
        'appKey': APP_KEY,
        'salt': uuid01,
        'sign': encrypt(signStr),
        'signtype': 'v3',
        'q': pig1
    }
    req4 = requests.post(url3, headers=head3, data=data3)
    print(req4.content)
    req = json.loads(req4.content)
    print(req)
    try:
        print(req['resRegions'])
    except Exception as e:
        print(Exception)
    return req



def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def run1(text1):
    uuid01 = str(uuid.uuid1())
    APP_KEY = '083a4adf60f03782'
    APP_SECRET = 'Hz48kvkjdkXU5v76U9uOR4x3CqWvHRIH'
    url3 = 'https://openapi.youdao.com/api'
    curtime = str(int(time.time()))
    signStr = APP_KEY + truncate(text1) + uuid01 + curtime + APP_SECRET
    text1 = text1.encode('utf-8')
    head3 = {'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    data3 = {
        'from': 'auto',
        'to': 'zh-CHS',
        'appKey': APP_KEY,
        'salt': uuid01,
        'sign': encrypt01(signStr),
        'signType': 'v3',
        'q': text1,
        'curtime': curtime
    }
    req4 = requests.post(url3, headers=head3, data=data3)
    print(req4.content)
    req = json.loads(req4.content)
    print(req)
    try:
        print(req['resRegions'])
    except Exception as e:
        print(Exception)
    return req


def xFunc2(event, canvas01, ans):
    global bmpinfo
    if event.x == bmpinfo[0] or event.y == bmpinfo[1]:
        return
    canvas01.delete("prscrn")
    canvas01.create_rectangle(bmpinfo[0], bmpinfo[1], event.x, event.y, fill='blue', outline='red', tag="prscrn")
    canvas01.grid(row=0, column=0)


def hello():
    mbox.showinfo(title='帮助信息', message='请联系管理员qq号：3485188464')  # 消息提醒弹窗，点击确定返回值为 ok


def zhubuju():
    frame1.grid_forget()
    frame3.grid_forget()
    frame2.grid_forget()


def jinruhide():
    zhubuju()
    app.geometry("300x300")

    frame_input.grid(row=0, column=0)
    frame_out.grid(row=1, column=0)
    framesxianshi.grid(row=0, column=0)
    input_text.grid(row=0, column=0)
    input_text.bind("<Return>", xianshi)
    hd = win32gui.FindWindow(0, "su翻")  # 根据标题找到窗口句柄
    win32gui.ShowWindow(hd, 0)  # 把句柄传给showwindow实现显示隐藏效果
    xxx = threading.Thread(target=thr1)
    xxx.daemon = True
    # 设置守护线程，当线程结束，守护线程同时关闭，要不然这个线程会一直运行下去。
    xxx.start()


def xianshi(event):

    string = input_text.get()
    print(string)
    req = run1(string)
    if req['errorCode'] == '0':
        tex = ''
        print(type(req['translation']))
        print(req['translation'])
        for i in range(0, len(req['translation'])):
            tex += req['translation'][i]
        ans.configure(text=tex)
        ans.grid(row=1, column=0)


def thr1():
    flag = 0
    win32gui.RegisterHotKey(0, 99, win32con.MOD_SHIFT + win32con.MOD_WIN, 0)
    win32gui.RegisterHotKey(0, 100, win32con.MOD_CONTROL, 0)
    while 1:
        time.sleep(1)  # 避免频繁获取暂停一秒
        msg = win32gui.GetMessage(0, 0, 0)  # 获得本线程产生的消息，返回值是个列表
        # msg-----[1, (0, 786, 99, 7929864, 24627051, (534, 440))]
        if msg[1][2] == 99:  # 根据下标和热键id确定按下的是我们注册的热键99
            jietu()
        if msg[1][2] == 100:  # 根据下标和热键id确定按下的是我们注册的热键100
            flag = not flag  # 更改标志
            hd = win32gui.FindWindow(0, "su翻")  # 根据标题找到窗口句柄
            win32gui.ShowWindow(hd, flag)  # 把句柄传给showwindow实现显示隐藏效果


app = Tk()
app01 = Toplevel()
app01.title('picture')
app01.iconify()

mark = 'error'
app.title('su翻')
textapp = ''  # cookies
# app.iconbitmap('favicon.ico')
text1 = '欢迎使用su翻，旨在打造最便捷的翻译使用工具'
text2 = '本客户端有任何意见，请点击帮助按钮联系作者，作者：lfh'
bmpinfo = [0, 0]
app.geometry("1000x540")
app.resizable(False, False)
frame1 = Frame(app, width=1000, height=28, bg='#DCE2F1')
biaotou = Label(frame1, text=text1, font=('楷体', 14), bg='#DCE2F1')
biaotou.grid(row=0, column=0)
bangzhu = Button(frame1, text='?帮助', font=('楷体', 14), width=6, height=1, command=hello)
bangzhu.grid(row=0, column=2, padx=500)

frame2 = Frame(app, width=1000, height=20, bg='#DCE2F1')
biaowei = Label(frame2, text=text2, font=('楷体', 12), bg='#DCE2F1')
biaowei.grid(row=0, column=1, padx=450)
frame3 = Frame(app, width=1000, height=480, bg='#DCE2F1')
b1 = Button(frame3, text='欢迎使用su翻', font=('楷体', 22), command=jinruhide)

b1.grid(row=1, column=1, padx=400, pady=200)
""" 文字翻译主界面 """
frame_input = Frame(app, width=200, height=50, pady=10)
input_text = Entry(frame_input, width=40, highlightcolor='blue', highlightthickness=1, selectborderwidth=10, justify=LEFT)
input_text.grid(row=0, column=0)
frame_out = Frame(app, width=290, height=250, pady=10)
framesxianshi = LabelFrame(frame_out, text="翻译内容", width=280, height=240, borderwidth=2)
ans = Label(framesxianshi, font=("JetBrains Mono", 10), fg='black')
framesxianshi.grid(row=0, column=0)
# frame_out.rowconfigure(0, weight=1)
# frame_out.columnconfigure(0, weight=1)
frame_input.grid(row=0, column=0)
frame_out.grid(row=1, column=0)
app.rowconfigure(0, weight=1)
app.columnconfigure(0, weight=1)

input_text.grid_remove()
frame_input.grid_remove()
frame_out.grid_remove()
framesxianshi.grid_remove()


# 主界面
frame3.grid(row=1, column=0)
frame3.grid_propagate(0)
frame1.grid(row=0, column=0)
frame1.grid_propagate(0)
frame2.grid(row=2, column=0)
frame2.grid_propagate(0)
app01.mainloop()
app.mainloop()
