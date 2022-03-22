from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
import program_db as db
import subprocess
import os
import time
import json

error_msg = []
#主窗口
class Program(tk.Tk):
    def __init__(self):
        super().__init__()
        self.path_j = StringVar()
        self.path_st = StringVar()
        self.path_fa = StringVar()
        self.QR_code = StringVar()  # 二维码sn
        self.dbstate =StringVar()
        self.value_save = IntVar()

        self.fa_name = StringVar()
        self.set_init_window()

        self.title("烧录工具_v1.0")  # 窗口名
        self.geometry('534x600+250+100')  # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置

        self.value_save.set(1)#设置初始为需要将数据存入数据库

    # 设置窗口
    def set_init_window(self):

        self.setting_data_button = Button(self, text="SETTING", command=self.get_setting)
        self.setting_data_button.grid(row=0, column=0, sticky=W)

        self.form_db_button = Button(self, text='db_SETTING', command=self.ask_program_db)
        self.form_db_button.grid(row=0, column=1, sticky=W)

        self.help_data_button = Button(self, text="HELP")
        self.help_data_button.grid(row=0, column=2, sticky=W)

        self.program_name_lable = Label(self, text='program file name:').grid(row=1, column=0, columnspan=2,sticky=W)
        self.program_msg_entry = Entry(self, textvariable=self.fa_name, state='readonly').grid(row=1, column=1, columnspan=2, sticky=EW)

        self.db_connect_lable = Label(self, text='db_connect:').grid(row=2, column=0, columnspan=2, sticky=W)
        self.db_connect_entry = Entry(self, textvariable=self.dbstate, state='readonly').grid(row=2, column=1, columnspan=2, sticky=EW)

        self.msg_QR_code_lable = Label(self, text='QR code：').grid(row=3, column=0,columnspan=2, sticky=W)
        self.msg_entry = Entry(self,textvariable=self.QR_code)
        self.msg_entry.grid(row=3, column=1, columnspan=2, sticky=EW)

        self.save_to_db_checkbutton = Checkbutton(self, text='save to database：', variable=self.value_save
        ,onvalue=1, offvalue=0)
        self.save_to_db_checkbutton.grid(row=4, column=0, sticky=W)

        self.program_button = Button(self, text='program', command=self.begin_program)  # 烧录按钮
        self.program_button.grid(row=4, column=1, sticky=EW)

        self.log_label = Label(self, text="日志")
        self.log_label.grid(row=5, column=0, sticky=W)

        self.log_data_Text = Text(self, width=80, height=40)  # 日志框
        self.log_data_Text.grid(row=6, column=0, columnspan=6)
        self.log_data_Text.tag_add('tag1', END)
        self.log_data_Text.tag_config('tag1', foreground='red')

    # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    #烧录
    def begin_program(self):
        print(self.value_save.get())
        print(self.QR_code.get())
        if(self.value_save.get()==0):#判断是否需要将错误信息存入数据库'0'为不需要，'1'为需要
            self.write_log_to_Text()
           
        else:
            db_connect = self.dbstate.get().split('--->')[0]
            if(db_connect=='连接失败'):
                self.log_data_Text.insert(END,'数据库连接失败，请检查并重新连接！！！','tag1')
            else:
                self.write_log_to_Text()


            pass


    # 日志打印
    def write_log_to_Text(self):

        global error_msg

    
        data = self.create_to_pro()
        current_time = self.get_current_time()

        # 清空error_msg
        msg_num = 0 #记录日志输出条数
        msg_cont = {}#将日志第6条以后的数据记录到字典中
        msg_cont['Error'] =''#初始化错误信息

        error_msg = []

        self.log_data_Text.delete(1.0, END)
        self.log_data_Text.insert(END, '-' * 30 + '开始烧录' + '-' * 30 + '\n')
        for msg in data:
            logmsg_in = str(current_time) + " " + msg + "\n"  # 换行
            self.log_data_Text.insert(END, logmsg_in)
            msg_num += 1
            #记录错误信息
            try:
                if (msg_num>6):
                    msg_cont[msg.split(':')[0]] = msg.split(':')[1]
            except:
                if (msg_num>6 and msg.lower().find('error') !=-1):
                    msg_cont['Error'] = 'Please check the setting again !!!'


        if(len(msg_cont['Error']) !=0):
            cont = 'Program Fail !!! --->'+msg_cont['Error']
            self.log_data_Text.insert(END, cont, 'tag1')
            



    # 访问setting
    def get_setting(self):

        res = self.ask_setting_dialog()

        if (res == None): return
        self.path_j = res.path1
        self.path_st = res.path2
        self.path_fa = res.path3

        if (self.path_fa != None):
            fa = self.path_fa.get().split('/')
            self.fa_name.set(fa[len(fa) - 1])
        else:
            self.fa_name.set(None)
        self.set_init_window()

    # 生成批处理文件并运行批处理文件进行烧录返回日志信息
    def create_to_pro(self):

        global error_msg
        # firmware_con = r'''echo off
        #    cd /d C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin
        #    STM32_Programmer_CLI.exe -C port=SWD freq=4000 -w "D:\ATE-work\Cefaly4_Enhance_v1.00.004.hex" -v -rst
        #    '''
        try:
            STM32_Link = self.path_st.get().rsplit('/', 1)

            STM32_file = STM32_Link[0]
            STM32_exe = STM32_Link[1]

            # 批处理文件内容
            firmware_con = 'echo off' + '\n' + 'cd /d' + '  ' + STM32_file + '  \n' + STM32_exe + ' -C port=SWD freq=4000 -w  ' + '"' + self.path_fa.get() + '  "' + '-v -rst'
            link_path_con = '{"' + 'path_st' + '"' + ':' + '"' + self.path_st.get() + '"' + ',' + '"' + 'path_fa' + '"' + ':' + '"' + self.path_fa.get() + '"}'

            # 写入一个临时文件
            fileName = 'Burn_testFirmware.bat'  # 批处理文件
            link_path = 'link_path.hex'
            filePath = os.path.join(os.getcwd(), 'bat')
            if not os.path.exists(filePath):
                os.mkdir(filePath)

            # 将批处理信息写入文件
            f = open(filePath + os.sep + fileName, 'w')
            f.write(firmware_con)
            f.close()
            # 将路径信息写入文件
            l = open(filePath + os.sep + link_path, 'w')
            l.write(link_path_con)
            l.close()

            # 执行BAT并定向输入(不出现黑窗口)
            p = subprocess.Popen(filePath + os.sep + fileName, stdout=subprocess.PIPE, shell=True,
                                 stderr=subprocess.STDOUT)
            data = []  # 日志信息
            curline = p.stdout.readlines()
            for cur in curline:
                data.append(cur.decode('gbk'))

            p.wait()
            p.kill()

            return data
        except Exception as create_to_pro_exception:
            print(create_to_pro_exception)
            error_msg.append(str(create_to_pro_exception))
            return error_msg
        pass

    # 生成子窗口
    def ask_setting_dialog(self):
        setting_dialog = Setting_dialog()
        self.wait_window(setting_dialog)
        return setting_dialog
    # 生成数据库设置窗口
    def ask_program_db(self):
        db_s = db.db_form()
        self.wait_window(db_s)

        if (db_s.dbstate =='连接成功'):
            self.dbstate.set(db_s.dbstate.get()+'--->'+db_s.host.get()+'：'+db_s.user.get()+':'+db_s.database.get())
        else:
            self.dbstate.set(db_s.dbstate.get() + '--->' + db_s.host.get() +'-->数据库:' + db_s.database.get())
            #self.dbstate=db_s.dbstate
            #self.dbstate.set(db_s.dbstate.get())

        self.set_init_window()
        return db_s



# 设置烧录程序和烧录内容路径子窗口
class Setting_dialog(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('setting')
        self.path1 = StringVar()
        self.path2 = StringVar()
        self.path3 = StringVar()
        self.setup_UI(None)
        self.set_def_path()

        self.title("烧录工具_setting")  # 窗口名
        self.geometry('300x120+50+50')  # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置

    def set_def_path(self):  # 设置默认路径

        fileName = 'link_path.hex'
        filePath = os.path.join(os.getcwd(), 'bat')
        if not os.path.exists(filePath):
            os.mkdir(filePath)
        try:

            f = open(filePath + os.sep + fileName, 'r')
            msg = f.readlines()
            json_path_link = json.loads(str(msg[0]))
            f.close()

            self.path2.set(json_path_link['path_st'])
            self.path3.set(json_path_link['path_fa'])
        except:
            val2 = 'C:/Program Files/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI.exe'
            val3 = "D:/ATE-work/Cefaly4_Enhance_v1.00.004.hex"
            self.path2.set(val2)
            self.path3.set(val3)

        pass

    def setup_UI(self, name):

        self.attributes('-topmost', True)

        if (name == 'j_link'):
            self.path1.set(askopenfilename())
            # print(self.path1.get())
        elif (name == 'st_link'):
            self.path2.set(askopenfilename())
            # print(self.path2.get())
        elif (name == 'framare'):
            self.path3.set(askopenfilename())
            # print(self.path3.get())

        v = IntVar()
        v.set(2)

        # j_link_path_radiobutton = Radiobutton(self, variable=v, text="j_link_path".format(1), value=1, )
        # j_link_path_radiobutton.grid(row=0, column=0)
        # j_link_path_inputFile = Entry(self, textvariable=self.path1).grid(row=0, column=1)
        # j_link_path_button = Button(self, text='路径选择', command=lambda:self.setup_UI('j_link')).grid(row=0, column=2)

        st_ling_path_radiobutton = Radiobutton(self, variable=v, text="st_ling_path".format(1), value=2, )
        st_ling_path_radiobutton.grid(row=1, column=0)
        st_ling_path_inputFile = Entry(self, textvariable=self.path2).grid(row=1, column=1)
        st_ling_path_button = Button(self, text='路径选择', command=lambda: self.setup_UI('st_link')).grid(row=1, column=2)

        framare_path_lable = Label(self, text="framare_path")
        framare_path_lable.grid(row=2, column=0)
        framare_path_inputFile = Entry(self, textvariable=self.path3).grid(row=2, column=1)
        framare_path_button = Button(self, text='路径选择', command=lambda: self.setup_UI('framare')).grid(row=2, column=2)

        OK_button = Button(self, text='确定', command=self.ok).grid(row=3, column=0)
        cancel_button = Button(self, text='取消', command=self.cancel).grid(row=3, column=1)

    def ok(self):
        self.destroy()

    def cancel(self):
        self.path1 = None
        self.path2 = None
        self.path3 = None
        self.destroy()


if __name__ == '__main__':
    app = Program()
    app.mainloop()
