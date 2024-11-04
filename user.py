# from my_import import *
import time
import tkinter as tk
import requests
import threading
from tkinter import Tk, Label, font
import os

get_chat_going = 1
beer_user_get_going = 1


def clear_widgets(window):
    """删除窗口中的所有控件"""
    for widget in window.winfo_children():
        widget.destroy()


def tk_label(window, text, x, y, width, height):
    lbl = tk.Label(window)
    lbl.config(text=text, font=font.Font(size=20))
    lbl.place(x=x, y=y, width=width, height=height)
    return lbl


def tk_entry(window, length, x, y, width, height):
    custom_font = font.Font(size=20)  # 例如，设置Arial字体，大小为14
    txt = tk.Entry(window, width=length, font=custom_font, justify='center')
    txt.place(x=x, y=y, width=width, height=height)
    return txt


def tk_button(window, text, command, x, y, width, height):
    custom_font = font.Font(size=20)  # 例如，设置Arial字体，大小为14
    but = tk.Button(window, text=text, command=command, font=custom_font, justify='center')
    but.place(x=x, y=y, width=width, height=height)
    return but


# 创建一个可滚动的文本框
def tk_text(window, x, y, width, height):
    # 创建一个Text widget
    text_widget = tk.Text(window, wrap=tk.WORD)

    # 创建一个垂直滚动条并与Text widget关联
    scroll_bar = tk.Scrollbar(window, command=text_widget.yview)

    # 将滚动条与Text widget配置在一起
    text_widget.configure(yscrollcommand=scroll_bar.set)

    # 布局滚动条和Text widget
    # scroll_bar.place(x=x, y=y+width-10, width=10, height=height)
    text_widget.place(x=x, y=y, width=width, height=height)

    return text_widget


def game_end(window):
    global get_chat_going
    global beer_user_get_going
    get_chat_going = 0
    beer_user_get_going = 0
    window.after(2000, lambda: window.quit())


# 用户注册页面
def creative_account(url, window):
    clear_widgets(window)

    lbl_name = tk_label(window, text="昵称：", x=166, y=115, width=200, height=50)
    txt_name = tk_entry(window, length=10, x=366, y=115, width=268, height=50)

    lbl_password = tk_label(window, text="密码：", x=166, y=195, width=200, height=50)
    txt_password = tk_entry(window, length=10, x=366, y=195, width=268, height=50)

    lbl_email = tk_label(window, text="邮箱：", x=166, y=275, width=200, height=50)
    txt_email = tk_entry(window, length=10, x=366, y=275, width=268, height=50)

    lbl_sign = tk_label(window, text="请输入昵称！", x=200, y=356, width=400, height=50)

    but_create_account = tk_button(window, text="注册", command=lambda: game_creative_account(url, window, lbl_sign, txt_name, txt_password, txt_email), x=166, y=436,
                                   width=200, height=50)
    but_create_account = tk_button(window, text="返回", command=lambda: game_start(url, window), x=434, y=436, width=200, height=50)


# 用户注册逻辑
def game_creative_account(url, window, lbl_sign, txt_name, txt_password, txt_email):
    name = txt_name.get()
    password = txt_password.get()
    email = txt_email.get()

    if name == '' or password == '' or email == '':
        lbl_sign.config(text="请输入完整信息！")
    else:
        data = {
            'name': name,
            'password': password,
            'email': email,
        }
        # 发送 POST 请求
        response = requests.post(url + '/create_count', json=data)

        response_json = response.json()

        # 输出时差和 Flask 服务器返回的数据
        print(f'Response from server: {response}')
        if response_json.get('status') == '创建用户成功！':
            lbl_sign.config(text="注册成功，即将返回登录！")
            window.after(1000, lambda: game_start(url, window))
        else:
            lbl_sign.config(text=response_json.get('status'))


# 用户登录页面
def game_start(url, window):
    clear_widgets(window)

    lbl_name = tk_label(window, "昵称：", 166, 145, 200, 50)
    lbl_password = tk_label(window, "密码：", 166, 225, 200, 50)

    txt_name = tk_entry(window, 10, 366, 145, 200, 50)
    txt_password = tk_entry(window, 10, 366, 225, 200, 50)
    txt_name.insert(0, "test")
    txt_password.insert(0, "test")

    lbl_sign = tk_label(window, text="请输入昵称！", x=234, y=325, width=400, height=50)

    but_ok = tk_button(window, text="登录", command=lambda: game_login(url, window, lbl_sign, txt_name, txt_password), x=166, y=406, width=200, height=50)

    but_create_account = tk_button(window, text="注册", command=lambda: creative_account(url, window), x=434, y=406, width=200, height=50)


# 用户登录逻辑
def game_login(url, window, lbl_sign, txt_name, txt_password):
    password = txt_password.get()
    name = txt_name.get()

    if name == '' or password == '':
        lbl_sign.config(text='请输入完整信息！')
    else:
        data = {
            'name': name,
            'password': password,
        }
        # 发送 POST 请求
        response = requests.post(url + '/login', json=data)
        response_json = response.json()
        print(f'Response from server: {response}')

        if response_json.get('status') == "登录成功":
            ID = response_json.get('id')
            login_successes(url, window, ID)
        else:
            lbl_sign.config(text=response_json.get('status'))


# 登录成功
def login_successes(url, window, ID):
    clear_widgets(window)

    lbl_sign = tk_label(window, text="登录成功！", x=200, y=115, width=400, height=50)
    lbl_id = tk_label(window, text="您的ID为：" + str(ID), x=200, y=195, width=400, height=50)

    but_go_back_login = tk_button(window, text="进入模拟系统", command=lambda: game_game(url, window, ID), x=200, y=275, width=400, height=50)
    but_go_back_login = tk_button(window, text="进入聊天室", command=lambda: game_chat(url, window, ID), x=200, y=355, width=400, height=50)
    but_exit = tk_button(window, "退出", command=lambda: game_end(window), x=200, y=435, width=400, height=50)


# 游戏初始化
def game_init(window):
    txt_IP = tk_entry(window, 20, 366, 145, 268, 50)
    txt_port = tk_entry(window, 10, 366, 225, 268, 50)
    txt_IP.insert(0, "www.xiaoxiaosky.top")
    txt_port.insert(0, "4444")

    lbl_IP = tk_label(window, "IP:", 166, 145, 200, 50)
    lbl_port = tk_label(window, "端口:", 166, 225, 200, 50)

    lbl_sign = tk_label(window, text="请输入IP和端口！", x=234, y=325, width=400, height=50)

    but_ok = tk_button(window, "确定", lambda: ip_config(window, lbl_sign, txt_IP, txt_port), 166, 406, 200, 50)
    but_exit = tk_button(window, "退出", command=lambda: game_end(window), x=434, y=406, width=200, height=50)


# IP配置
def ip_config(window, lbl_sign, txt_ip, txt_port):
    ip = txt_ip.get()
    port = txt_port.get()

    if ip == '' or port == '':
        lbl_sign.config(text='请输入完整信息！')
    else:
        url = 'http://' + ip + ':' + port  # + '/'
        data = {'message': 'test'}
        # 设置超时时间为5秒，可以根据需要调整
        timeout_seconds = 1
        try:
            response = requests.post(url + '/connect_test', json=data, timeout=timeout_seconds)
            response_json = response.json()

            if response_json.get('status') == "连接成功！":
                lbl_sign.config(text='连接成功！')
                game_start(url, window)
            else:
                lbl_sign.config(text='连接失败！')
        except requests.exceptions.Timeout:
            # 如果请求超时，捕获异常并处理
            lbl_sign.config(text='连接超时，请检查网络或服务器状态！')
        except requests.exceptions.RequestException as e:
            # 其他类型的请求异常也可以在这里处理
            lbl_sign.config(text=f'发生错误: {e}')


def game_beer(url, window, ID):
    clear_widgets(window)
    lbl_sign = tk_label(window, text="欢迎进入 模拟啤酒供应链 系统", x=0, y=60, width=800, height=50)
    lbl_id = tk_label(window, text="您的ID为：" + str(ID), x=600, y=60, width=200, height=50)

    lbl_id = tk_label(window, text="请输入队伍编号：", x=50, y=165, width=300, height=50)
    lbl_user = tk_label(window, text="请输入选定角色：", x=50, y=245, width=300, height=50)

    lbl_sign = tk_label(window, text="请输入队伍编号！", x=200, y=325, width=400, height=50)
    # lbl_group = tk_label(window, text="当前队伍状态", x=50, y=405, width=700, height=110)

    txt_group_id = tk_entry(window, 10, 350, 165, 400, 50)
    txt_group_user = tk_entry(window, 10, 350, 245, 400, 50)

    but_exit = tk_button(window, text="确定", command=lambda: game_beer_send(url, window, ID, txt_group_id, txt_group_user, lbl_sign), x=200, y=520, width=200,
                         height=50)
    but_exit = tk_button(window, text="退出", command=lambda: game_start(url, window), x=400, y=520, width=200, height=50)


def game_chat(url, window, ID):
    clear_widgets(window)
    lbl_hello = tk_label(window, text="欢迎进入信息交易场所！", x=0, y=0, width=800, height=50)
    lbl_id = tk_label(window, text="您的ID为：" + str(ID), x=600, y=0, width=200, height=50)
    lbl_id = tk_label(window, text="待发送", x=0, y=50, width=100, height=50)
    txt_chat = tk_entry(window, 5, 100, 50, 300, 50)

    lbl_sign = tk_label(window, text="请输入以了解的消息！", x=0, y=166, width=400, height=50)
    lbl_history = tk_label(window, text="打听到的消息记录", x=400, y=50, width=400, height=50)
    # lbl_chat_history = tk_label(window, text="聊天记录", x=400, y=100, width=400, height=500)
    text_chat_history = tk_text(window, x=400, y=100, width=400, height=500)

    lbl_note = tk_label(window, text="记事本", x=0, y=224, width=400, height=50)
    text_note = tk_text(window, 0, 282, 400, 318)

    # 创建一个Thread对象，将my_function作为目标函数，并传递参数
    new_thread = threading.Thread(target=request_chat, args=(url, window, text_chat_history, " "))

    # 启动新线程
    new_thread.start()

    # request_after(url, window, text_chat_history, " ")

    but_send = tk_button(window, text="发送", command=lambda: game_send(url, window, ID, txt_chat, lbl_sign, text_chat_history), x=0, y=108, width=200, height=50)
    # but_exit = tk_button(window, text="打听消息", command=lambda: request_chat(url, window,
    # text_chat_history, text_chat_history.get("1.0", tk.END)), x=200, y=108, width=200, height=50)
    but_exit = tk_button(window, text="退出", command=lambda: game_end(window), x=200, y=108, width=200, height=50)


def request_chat(url, window, text_chat_history, old_chat_message):
    global get_chat_going
    old_chat_message = ""
    while get_chat_going == 1:

        response = requests.post(url + '/get_chat', json={'num': 500})
        response_json = response.json()
        # print(response_json)
        chat_message = ""
        for chat in response_json:
            chat_message += chat['name'] + ': ' + chat['message'] + '\n'
            # print(chat)
        if chat_message != old_chat_message:
            old_chat_message = chat_message
            text_chat_history.delete(1.0, tk.END)
            text_chat_history.insert(tk.END, chat_message)

        # return chat_message
        time.sleep(1)


def game_send(url, window, ID, txt_chat, lbl_sign, text_chat_history):
    chat = txt_chat.get()
    is_ok = 0

    if chat == '':
        lbl_sign.config(text="请输入聊天内容！")
        is_ok = 0
    else:
        is_ok = 1

    data = {
        'id': ID,
        'message': chat,
    }

    if is_ok == 1:
        # 发送 POST 请求
        response = requests.post(url + '/create_chat', json=data)
        response_json = response.json()
        # 服务器返回数据
        # return_json = {
        #     'status': 'ok',
        #     'id': match[0],
        # }
        # Flask 服务器返回的数据
        print(f'Response from server: {response}')

        if response_json.get('status') == "成功发送消息！":
            lbl_sign.config(text="发送成功！")
            text_chat_history.insert("1.0", "you: " + chat + '\n')
        else:
            # print(response_json)
            lbl_sign.config(text=response_json.get('status'))


def game_game(url, window, ID):
    clear_widgets(window)
    lbl_sign = tk_label(window, text="欢迎进入系统！", x=0, y=60, width=800, height=50)
    lbl_id = tk_label(window, text="您的ID为：" + str(ID), x=600, y=60, width=200, height=50)

    but_sys1 = tk_button(window, text="啤酒供应链", command=lambda: game_beer(url, window, ID), x=100, y=160, width=200, height=50)
    # but_sys2 = tk_button(window, text="橙子（待开发）", command=lambda: game_null(url, window, ID), x=100, y=240, width=200, height=50)
    # but_sys3 = tk_button(window, text="（待开发）", command=lambda: game_null(url, window, ID), x=100, y=320, width=200, height=50)
    # but_sys4 = tk_button(window, text="（待开发）", command=lambda: game_null(url, window, ID), x=300, y=160, width=200, height=50)
    # but_sys5 = tk_button(window, text="（待开发）", command=lambda: game_null(url, window, ID), x=300, y=240, width=200, height=50)
    # but_sys6 = tk_button(window, text="（待开发）", command=lambda: game_null(url, window, ID), x=300, y=320, width=200, height=50)
    # but_sys7 = tk_button(window, text="（待开发）", command=lambda: game_null(url, window, ID), x=500, y=160, width=200, height=50)
    # but_sys8 = tk_button(window, text="（待开发）", command=lambda: game_null(url, window, ID), x=500, y=240, width=200, height=50)
    # but_sys9 = tk_button(window, text="（待开发）", command=lambda: game_null(url, window, ID), x=500, y=320, width=200, height=50)

    but_exit = tk_button(window, text="退出", command=lambda: game_start(url, window), x=200, y=430, width=400, height=50)


def game_null(url, window, ID):
    clear_widgets(window)
    lbl_sign = tk_label(window, text="欢迎进入（待开发）系统！", x=0, y=60, width=800, height=50)
    lbl_id = tk_label(window, text="您的ID为：" + str(ID), x=600, y=60, width=200, height=50)

    lbl_id = tk_label(window, text="请输入队伍编号：", x=50, y=165, width=300, height=50)
    lbl_id = tk_label(window, text="请输入选定角色：", x=50, y=245, width=300, height=50)
    # lbl_id = tk_label(window, text="当前队伍状态", x=50, y=295, width=700, height=220)

    txt_group_id = tk_entry(window, 10, 350, 165, 400, 50)
    txt_group_id = tk_entry(window, 10, 350, 245, 400, 50)

    but_exit = tk_button(window, text="确定", command=lambda: game_start(url, window), x=200, y=520, width=200, height=50)
    but_exit = tk_button(window, text="退出", command=lambda: game_start(url, window), x=400, y=520, width=200, height=50)


def game_beer_send(url, window, ID, txt_group_id, txt_group_user, lbl_sign):
    group_id = txt_group_id.get()
    group_user = txt_group_user.get()
    is_ok = 0

    if group_id == '' or group_user == '':
        lbl_sign.config(text='请输入完整信息！')
        is_ok = 0
    else:
        # 1工厂    +2供应商A     + 4分销商A
        #                      + 5分销商B
        #         +3供应商B     + 6分销商C
        #                      + 7分销商D
        if 1 <= int(group_user) <= 7:
            is_ok = 1
        else:
            lbl_sign.config(text='角色选择错误！')
            is_ok = 0

    users = ['工厂', '供应商A', '供应商B', '分销商A', '分销商B', '分销商C', '分销商D']

    data = {
        'id': ID,
        'group_id': group_id,
        'group_user': users[int(group_user) - 1]
    }

    if is_ok == 1:
        # 发送 POST 请求
        response = requests.post(url + '/beer_login', json=data)
        response_json = response.json()
        # Flask 服务器返回的数据
        print(f'Response from server: {response}')

        if response_json.get('status') == "角色登录成功！":
            lbl_sign.config(text="角色登录成功！准备进入系统！")
            window.after(1000, lambda: game_beer_weight(url, window, ID, group_id, users[int(group_user) - 1]))
        else:
            lbl_sign.config(text=response_json.get('status'))


def game_beer_weight(url, window, ID, group_id, group_user):
    clear_widgets(window)
    lbl_title = tk_label(window, text="欢迎进入啤酒供应链系统！", x=0, y=23, width=800, height=50)
    lbl_id = tk_label(window, text="您的ID为：" + str(ID), x=600, y=73, width=200, height=50)
    lbl_group = tk_label(window, text="当前队伍:" + str(group_id), x=0, y=73, width=400, height=50)

    lbl_user = tk_label(window, text="当前角色：", x=50, y=130, width=300, height=50)
    lbl_sign_sign = tk_label(window, text="当前队伍状态：", x=50, y=200, width=300, height=50)
    lbl_user_user = tk_label(window, text=str(group_user), x=350, y=130, width=400, height=50)
    lbl_sign = tk_label(window, text="等待队友中...", x=350, y=200, width=400, height=50)

    lbl_工厂 = tk_label(window, text="工厂(未知)", x=100, y=367, width=200, height=50)
    lbl_供应商A = tk_label(window, text="供应商A(未知)", x=300, y=317, width=200, height=50)
    lbl_供应商B = tk_label(window, text="供应商B(未知)", x=300, y=417, width=200, height=50)
    lbl_分销商A = tk_label(window, text="分销商A(未知)", x=500, y=267, width=200, height=50)
    lbl_分销商B = tk_label(window, text="分销商B(未知)", x=500, y=317, width=200, height=50)
    lbl_分销商C = tk_label(window, text="分销商C(未知)", x=500, y=417, width=200, height=50)
    lbl_分销商D = tk_label(window, text="分销商D(未知)", x=500, y=467, width=200, height=50)
    but_exit = tk_button(window, text="退出", command=lambda: game_start(url, window), x=300, y=534, width=200, height=50)

    # 创建一个Thread对象，将my_function作为目标函数，并传递参数
    new_thread = threading.Thread(target=beer_user_get,
                                  args=(
                                      url, window, ID, lbl_sign, group_id, group_user,
                                      lbl_工厂, lbl_供应商A, lbl_供应商B, lbl_分销商A, lbl_分销商B,
                                      lbl_分销商C, lbl_分销商D, but_exit))

    # 启动新线程
    new_thread.start()


def beer_user_get(url, window, ID, lbl_sign, group_id, group_user, lbl_工厂, lbl_供应商A, lbl_供应商B, lbl_分销商A, lbl_分销商B, lbl_分销商C, lbl_分销商D, but_exit):
    global beer_user_get_going
    beer_user_get_going = 1
    data = {
        'id': ID,
        'group_id': group_id,
        'group_user': group_user
    }
    while beer_user_get_going == 1:
        response = requests.post(url + '/beer_get_group_user', json=data)
        response_json = response.json()
        print(response_json)

        {
         "faces": [{"face_token": "bcfe7f64c2cc5a322952807df6972c72",
                    "face_rectangle": {"top": 147, "left": 260, "width": 263, "height": 263},
                    "attributes": {"gender": {"value": "Male"}, "age": {"value": 23},
                                   "beauty": {"male_score": 61.473, "female_score": 58.274}
                                   }
                    }],
         "image_id": "Z+Oo/RVKKEQDu0kqaTVzwQ==", "face_num": 1}

        {"request_id": "1727238608,96826569-9e59-4770-948a-6873b9c00411",
         "time_used": 299,
         "faces": [{"face_token": "b9bb2b127a80813c280d474cd0f7657d",
                    "face_rectangle": {"top": 205, "left": 173, "width": 274, "height": 274},
                    "attributes": {"gender": {"value": "Male"}, "age": {"value": 20},
                                   "beauty": {"male_score": 65.595, "female_score": 57.557}}}],
         "image_id": "4Bs9wB0nyt8vgk5gdutWVA==", "face_num": 1}

        response_json.get('faces')[0].get('attributes').get('beauty').get('male_score')
        response_json.get('faces')[0].get('attributes').get('beauty').get('female_score')


        lbl_工厂.config(text="工厂：" + response_json.get('工厂'))
        lbl_供应商A.config(text="供应商A：" + response_json.get('供应商A'))
        lbl_供应商B.config(text="供应商B：" + response_json.get('供应商B'))
        lbl_分销商A.config(text="分销商A：" + response_json.get('分销商A'))
        lbl_分销商B.config(text="分销商B：" + response_json.get('分销商B'))
        lbl_分销商C.config(text="分销商C：" + response_json.get('分销商C'))
        lbl_分销商D.config(text="分销商D：" + response_json.get('分销商D'))

        if response_json.get('status') == "查询成功" and response_json.get('users') != 7:
            lbl_sign.config(text=f"等待队友中... 还差 {7 - response_json.get('users')} 人")
        else:
            beer_user_get_going = 0
            lbl_sign.config(text="队伍已满，请按确认进入系统！")
            but_enter = tk_button(window, text="进入系统", command=lambda: game_beer_data(url, window, ID, group_id, group_user), x=200, y=534, width=200, height=50)
            # but_enter = tk_button(window, text="进入系统", command=lambda: game_beer_start(url, window, ID, group_id, group_user,lbl_sign), x=200, y=534, width=200,
            # height=50)
            but_exit.place(x=400, y=534)

        # print(beer_user_get_going)
        time.sleep(1)


# def game_beer_start(url, window, ID, group_id, group_user, lbl_sign):
#     data = {
#         'id': ID,
#         'group_id': group_id,
#         'group_user': group_user
#     }
#     response = requests.post(url + '/beer_start', json=data)
#
#     if response.json().get('status') == "开始游戏":
#         game_beer_data(url, window, ID, group_id, group_user)
#     else:
#         print(response.json().get('status'))
#         lbl_sign.config(text=response.json().get('status'))


def game_beer_data(url, window, ID, group_id, group_user):
    clear_widgets(window)
    lbl_title = tk_label(window, text="欢迎进入啤酒供应链系统！", x=0, y=0, width=800, height=50)
    lbl_week = tk_label(window, text="第1周", x=0, y=0, width=200, height=50)
    lbl_id = tk_label(window, text="您的ID为：" + str(ID), x=600, y=0, width=200, height=50)
    lbl_group = tk_label(window, text="队伍:" + str(group_id), x=0, y=50, width=400, height=50)
    lbl_user = tk_label(window, text="角色：" + str(group_user), x=400, y=50, width=400, height=50)
    lbl_sign = tk_label(window, text="请填写信息！", x=200, y=200, width=400, height=50)
    lbl_time = tk_label(window, text="剩余时间：", x=0, y=100, width=400, height=50)

    lbl_dinghuo = tk_label(window, text="订货量", x=400, y=100, width=200, height=50)

    lbl_fahuoA = tk_label(window, text="发货A", x=0, y=150, width=200, height=50)
    lbl_fahuoB = tk_label(window, text="发货B", x=400, y=150, width=200, height=50)

    txt_dinghuo = tk_entry(window, 10, 600, 100, 200, 50)
    txt_fahuoA = tk_entry(window, 10, 200, 150, 200, 50)
    txt_fahuoB = tk_entry(window, 10, 600, 150, 200, 50)

    FaHuoA = "供应商A"
    FaHuoB = "供应商B"

    if group_user == '工厂':
        FaHuoA, FaHuoB = "供应商A", "供应商B"

    elif group_user == '供应商A':
        FaHuoA, FaHuoB = "分销商A", "分销商B"

    elif group_user == '供应商B':
        FaHuoA, FaHuoB = "分销商C", "分销商D"

    elif group_user == '分销商A':
        FaHuoA, FaHuoB = "市场A", "市场B"
    elif group_user == '分销商B':
        FaHuoA, FaHuoB = "市场C", "市场D"
    elif group_user == '分销商C':
        FaHuoA, FaHuoB = "市场E", "市场F"
    elif group_user == '分销商D':
        FaHuoA, FaHuoB = "市场G", "市场H"

    lbl_fahuoA.config(text=f"{FaHuoA} 发货量")
    lbl_fahuoB.config(text=f"{FaHuoB} 发货量")

    text_sign = tk_text(window, x=0, y=250, width=800, height=350)

    but_send = tk_button(window, text="发送",
                         command=lambda: game_beer_send_data(url, window, ID, group_id, group_user, lbl_week, lbl_sign, txt_dinghuo, txt_fahuoA, txt_fahuoB, text_sign),
                         x=0, y=200, width=200, height=50)
    but_exit = tk_button(window, text="退出", command=lambda: game_end(window), x=600, y=200, width=200, height=50)

    text_sign.insert(tk.END, f"    |{FaHuoA}                 |{FaHuoB}                 |          |上游                    |   \n")
    text_sign.insert(tk.END, "周期 订货量 发货量 累计欠货 订货量 发货量 累计欠货 期初库存量 送货量 累计欠货量 订货量 期末库存量 本期利润\n")


# # 订货量	发货量	累计欠货	订货量	发货量	累计欠货	期初库存量	送货量	累计欠货量	订货量	期末库存量	本期利润
#     |市场A                 |市场B                 |          |上游                    |
# 周期 订货量 发货量 累计欠货 订货量 发货量 累计欠货 期初库存量 送货量 累计欠货量 订货量 期末库存量 本期利润


def game_beer_send_data(url, window, ID, group_id, group_user, lbl_week, lbl_sign, txt_dinghuo, txt_fahuoA, txt_fahuoB, text_sign):
    pass

    # dinghuo = txt_dinghuo.get()
    # fahuoA = txt_fahuoA.get()
    # fahuoB = txt_fahuoB.get()
    # is_ok = 0
    #
    # if dinghuo == '' or fahuoA == '' or fahuoB == '':
    #     lbl_sign.config(text='请输入完整信息！')
    #     is_ok = 0
    # else:
    #     is_ok = 1
    #
    # data = {
    #     'id': ID,
    #     'group_id': group_id,
    #     'group_user': group_user,
    #     'dinghuo': dinghuo,
    #     'fahuoA': fahuoA,
    #     'fahuoB': fahuoB,
    # }
    #
    # if is_ok == 1:
    #     # 发送 POST 请求
    #     response = requests.post(url + '/beer_login', json=data)
    #     response_json = response.json()
    #     # Flask 服务器返回的数据
    #     print(f'Response from server: {response}')
    #
    #     if response_json.get('status') == "角色登录成功！":
    #         lbl_sign.config(text="角色登录成功！准备进入系统！")
    #         window.after(1000, lambda: game_beer_weight(url, window, ID, group_id, users[int(group_user) - 1]))
    #     else:
    #         lbl_sign.config(text=response_json.get('status'))
    #
    # pass


def create_main_window():
    # app = Application()
    #
    # # 在主循环之后，你可以检查is_window_closed变量来判断窗口是否被关闭
    # if app.is_window_closed:
    #     print("窗口已关闭")
    # else:
    #     print("窗口仍然存在")
    """创建并初始化主窗口"""
    main_window = tk.Tk()
    # main_window = Application()
    main_window.title("Main Window")
    main_window.geometry("800x600")
    game_init(main_window)
    # game_start('http://www.xiaoxiaosky.top:4444', main_window)
    return main_window


def main():
    main_window = create_main_window()

    # 开始事件循环
    main_window.mainloop()


if __name__ == "__main__":
    main()
