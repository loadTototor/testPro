from tkinter import *
import tkinter as tk
import read_write_dict as wrd
import pymysql

dbxml = []


class db_form(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.host = StringVar()  # 连接地址
        self.user = StringVar()  # 连接用户名
        self.password = StringVar()  # 用户密码
        self.database = StringVar()  # 数据库名称
        self.dbstate = StringVar()  # 数据库连接状态

        self.getdb()  # 初始化数据库连接信息
        self.db_connect()
        self.set_UI()

        self.title("db_form")  # 窗口名
        self.geometry('300x150+400+300')  # 300 120为窗口大小，+50 +50 定义窗口弹出时的默认展示位置

    # 将数据库的连接信息保存在本地
    def set_UI(self):

        self.attributes('-topmost', True)
        self.host_lable = Label(self, text='host:').grid(row=0, column=0, sticky=W)
        self.host_entry = Entry(self, textvariable=self.host).grid(row=0, column=1)

        self.user_lable = Label(self, text='user:').grid(row=1, column=0, sticky=W)
        self.user_entry = Entry(self, textvariable=self.user).grid(row=1, column=1)

        self.password_lable = Label(self, text='password:').grid(row=2, column=0, sticky=W)
        self.password_entry = Entry(self, textvariable=self.password, show='*').grid(row=2, column=1)

        self.database_lable = Label(self, text='database:').grid(row=3, column=0, sticky=W)
        self.database_entry = Entry(self, textvariable=self.database).grid(row=3, column=1)

        self.dbstate_lable = Label(self, text='dbstate:').grid(row=4, column=0, sticky=W)
        self.dbstate_entry = Entry(self, textvariable=self.dbstate, fg='red', state='readonly')
        self.dbstate_entry.grid(row=4, column=1)

        self.db_link_button = Button(self, text='连接测试', command=self.db_connect).grid(row=5, column=0)

        self.db_link_button = Button(self, text='关闭窗口', command=self.win_close).grid(row=5, column=1)

        if (self.dbstate.get() == '连接成功'):
            self.dbstate_entry.configure(fg='green')
        else:
            self.dbstate_entry.configure(fg='red')

    # 初始化数据库连接信息
    def getdb(self):
        global dbxml
        try:
            filepath = 'settings'
            filename = 'db_msg.json'
            dbxml = wrd.read_get_json(filepath, filename)
            self.host.set(dbxml['host'])
            self.user.set(dbxml['user'])
            self.password.set(dbxml['password'])
            self.database.set(dbxml['database'])

        except Exception as e:
            dbxml = {'host': '', 'user': '', 'password': '', 'database': ''}
            self.host.set(dbxml['host'])
            self.user.set(dbxml['user'])
            self.password.set(dbxml['password'])
            self.database.set(dbxml['database'])

    def setdb(self):
        global dbxml
        try:
            filepath = 'settings'
            filename = 'db_msg.json'
            dbxml = {'host': self.host.get(),
                     'user': self.user.get(),
                     'password': self.password.get(),
                     'database': self.database.get()}
            dbxml = wrd.write_to_json(filepath, filename, dbxml)

        except Exception as e:
            print(e)

    def db_connect(self):
        self.setdb()
        try:
            db = pymysql.connect(host=self.host,
                                 user=self.user,
                                 password=self.password,
                                 database=self.database)
            self.dbstate.set('连接成功')
            return db
        except Exception as e:

            print(e)
            self.dbstate.set('连接失败')
        pass

    def win_close(self):

        self.destroy()
        pass


if __name__ == '__main__':
    db = db_form()
    db.mainloop()
