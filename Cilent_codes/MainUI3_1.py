import sys
import SettingOperations
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import re

import LoginAndGetMail2_6

class MainUI(QWidget):



    def __init__(self):
        # 初始化————init__
        super().__init__()
        self.initMainUI()

    def initMainUI(self):
        # debug 解决点击控件和窗口拖拽事件冲突造成的系统崩溃
        # 添加bool变量确定鼠标是否按在QWidget界面
        self.isPressedWidget = False
        # 设置widget组件的大小(w,h)
        self.resize(1000, 700)
        # 设置widget大小不可变
        self.setMinimumSize(1000, 700)
        self.setMaximumSize(1000, 700)
        # 设置widget组件的位置居中
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # 给widget组件设置标题
        self.setWindowTitle('圆桌清道夫')
        # 隐藏边框
        self.setWindowFlag(Qt.FramelessWindowHint)

        #创建子进程


        # 设置字体信息
        # 用于左侧选择栏的字体
        fontleft = QFont()
        # 字体
        fontleft.setFamily('微软雅黑')
        # 加粗
        fontleft.setBold(True)
        # 大小
        fontleft.setPointSize(15)
        fontleft.setWeight(75)

        # 左侧布局
        # 左侧按钮栏背景
        self.backgroundLeft = QLabel(self)
        self.backgroundLeft.setGeometry(QRect(0, 0, 250, 700))
        self.backgroundLeft.setStyleSheet('background-color: rgb(1,114,171)')

        # 左侧共三个按钮
        # 消息按钮，初始默认为按下
        self.btnleft_Message = QPushButton(self)
        self.btnleft_Message.setGeometry(0, 100, 250, 75)
        self.btnleft_Message.setText("      邮件")
        self.icon1 = QIcon()
        self.icon1.addPixmap(QPixmap("pic\Message.png"), QIcon.Normal, QIcon.Off)
        self.btnleft_Message.setIcon(self.icon1)
        self.btnleft_Message.setIconSize(QSize(50, 80))
        self.btnleft_Message.setStyleSheet("QPushButton{color:white}"
                                           "QPushButton{background-color:rgb(1,114,171)}"
                                           "QPushButton:hover{background-color:rgb(3,96,142)}"
                                           "QPushButton{border:none;}")
        self.btnleft_Message.setFont(fontleft)
        self.btnleft_Message.clicked.connect(self.Shift_Main)

        # 过滤器按钮，实现过滤器功能
        self.btnleft_Filter = QPushButton(self)
        self.btnleft_Filter.setGeometry(0, 175, 250, 75)
        self.btnleft_Filter.setText("   过滤器")
        self.icon2 = QIcon()
        self.icon2.addPixmap(QPixmap("pic\Filter.png"), QIcon.Normal, QIcon.Off)
        self.btnleft_Filter.setIcon(self.icon2)
        self.btnleft_Filter.setIconSize(QSize(50,80))
        self.btnleft_Filter.setStyleSheet("QPushButton{color:white}"
                                           "QPushButton{background-color:rgb(1,114,171)}"
                                           "QPushButton:hover{background-color:rgb(3,96,142)}"
                                           "QPushButton{border:none;}")
        self.btnleft_Filter.setFont(fontleft)
        self.btnleft_Filter.clicked.connect(self.Shift_Filter)
        # 设置为不可使用

        # 设置按钮，用于设置界面以及部分功能
        self.btnleft_Setting = QPushButton(self)
        self.btnleft_Setting.setGeometry(0, 250, 250, 75)
        self.btnleft_Setting.setText("      设置")
        self.icon3 = QIcon()
        self.icon3.addPixmap(QPixmap("pic\Setting.png"), QIcon.Normal, QIcon.Off)
        self.btnleft_Setting.setIcon(self.icon3)
        self.btnleft_Setting.setIconSize(QSize(50,80))
        self.btnleft_Setting.setStyleSheet("QPushButton{color:white}"
                                           "QPushButton{background-color:rgb(1,114,171)}"
                                           "QPushButton:hover{background-color:rgb(3,96,142)}"
                                           "QPushButton{border:none;}")
        self.btnleft_Setting.setFont(fontleft)
        self.btnleft_Setting.clicked.connect(self.Shift_Setting)
        # 设置为不可使用

        # 关于我们，显示项目介绍

        # 可能未来会有更多按钮？

        # 右侧布局
        # 右侧消息框背景
        self.backgroundRight = QLabel(self)
        self.backgroundRight.setGeometry(QRect(250, 0, 750, 700))
        self.backgroundRight.setStyleSheet('background-color: rgb(255, 255, 255)')

        # 设置关闭按钮
        self.closebtn = QPushButton('×', self)
        self.closebtn.setGeometry(950, 0, 50, 40)
        self.closebtn.setStyleSheet("QPushButton{color:black}"
                                    "QPushButton:hover{background-color:rgb(255, 0, 0)}"
                                    "QPushButton:hover{color:white}"
                                    "QPushButton{background-color:rgb(255, 255, 255)}"
                                    "QPushButton{border:none;}")
        self.closebtn.setFont(fontleft)
        self.closebtn.clicked.connect(self.hide)

        # 设置最小化按钮
        self.minimize = QPushButton('-', self)
        self.minimize.setGeometry(900, 0, 50, 40)
        self.minimize.setStyleSheet("QPushButton{color:black}"
                                    "QPushButton:hover{background-color:rgb(225, 225, 225)}"
                                    "QPushButton{background-color:rgb(255, 255, 255)}"
                                    "QPushButton{border:none;}")
        self.minimize.setFont(fontleft)
        self.minimize.clicked.connect(self.showMinimized)

        # 右侧布局一
        # 显示垃圾邮件信息
        # 每接受一条信息就创建一个新的Lable用于显示
        # 创建主界面布局
        self.Message_Receive = QFrame(self)
        self.Message_Receive.setGeometry(250, 40, 700, 660)
        self.vbox1 = QVBoxLayout(self.Message_Receive)
        self.listmodel1 = QStringListModel(self.Message_Receive)
        self.listview1 = QListView(self.Message_Receive)
        self.listview1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置说明栏
        tplt = "{0:{3}^30}\t{1:{3}^20}\t{2:{3}^20}"
        self.item1=[]
        self.item1.append(tplt.format('发件人','主要内容','判断结果',chr(12288)))

        self.listmodel1.setStringList(self.item1)
        self.listview1.setModel(self.listmodel1)
        self.vbox1.addWidget(self.listview1)



        # 右侧布局二
        # 显示过滤器信息
        # 创建过滤器及其窗体信息
        self.FilterFrame = QFrame(self)
        self.FilterFrame.setGeometry(250, 40, 700, 660)
        self.formLayout1 = QFormLayout(self.FilterFrame)

        # 设置标签
        self.addresser2 = QLabel(self)
        self.addresser2.setText("收件人")
        self.word_detect = QLabel(self)
        self.word_detect.setText("包含字词")

        # 设置文本框
        self.addresser2_text = QLineEdit(self)
        self.word_detect_text = QLineEdit(self)

        # 设置单选按钮
        self.spam_mail_button = QRadioButton("设置为垃圾邮件", self)
        self.normal_mail_button = QRadioButton("设置为为正常邮件", self)
        self.star_mail_button = QRadioButton("标记该类邮件", self)

        self.ButtonGroup = QButtonGroup(self)
        self.ButtonGroup.addButton(self.spam_mail_button, 1)
        self.ButtonGroup.addButton(self.normal_mail_button, 2)
        self.ButtonGroup.addButton(self.star_mail_button, 3)



        # 初始化单选按钮结果
        self.info = ""

        # 设置按钮
        self.Filter_create_button = QPushButton("创建过滤器", self)

        # 设置按钮事件
        # self.Filter_create_button.clicked.connect(self.Filter_create)

        # 过滤器界面布局
        self.formLayout1.addRow(self.addresser2, self.addresser2_text)
        self.formLayout1.addRow(self.word_detect, self.word_detect_text)
        self.formLayout1.addRow(self.spam_mail_button)
        self.formLayout1.addRow(self.normal_mail_button)
        self.formLayout1.addRow(self.star_mail_button)
        self.formLayout1.addRow(self.Filter_create_button)

        # 设置该窗口初始化时不可见
        self.FilterFrame.setVisible(False)

        # 右侧布局三
        # 显示设置信息
        self.SettingFrame = QFrame(self)
        self.SettingFrame.setGeometry(250, 40, 700, 660)
        self.formLayout2 = QFormLayout(self.SettingFrame)

        # # 设置说明栏
        # self.Receiving_rules = QLabel(self)
        # self.Receiving_rules.setText("        收信规则")
        # self.operation = QLabel(self)
        # self.operation.setText("                                                   操作")

        # 设置界面布局
        # self.formLayout2.addRow(self.Receiving_rules, self.operation)

        # 设置该窗口初始化时不可见
        self.SettingFrame.setVisible(False)
        # 2019/9/2 15:20 丁婧伊 设置界面加上过滤强度的选择
        # 获取本地文件存储的过滤强度
        temp = SettingOperations.Setting_Operations()
        intensity = temp.getIntensity()

        # 初始化过滤强度标签
        self.intensity_label = QLabel(self)
        self.intensity_label.setText("设置过滤强度：")
        self.final_intensity_label = QLabel(self)
        self.final_intensity_label.setText(intensity)
        self.formLayout2.addRow(self.intensity_label, self.final_intensity_label)

        # 过滤强度滑块，设置滑块的最大最小值和刻度间隔、位置
        self.intensity_slider = QSlider(Qt.Horizontal)
        self.intensity_slider.setMinimum(1)
        self.intensity_slider.setMaximum(100)
        self.intensity_slider.setSingleStep(2)
        self.intensity_slider.setTickInterval(33)
        self.intensity_slider.setTickPosition(QSlider.TicksAbove)
        self.formLayout2.addRow(self.intensity_slider)

        # 初始化滑块位置
        if (self.final_intensity_label.text() == "低强度"):
            self.intensity_slider.setValue(15)
        elif (self.final_intensity_label.text() == "中强度"):
            self.intensity_slider.setValue(50)
        else:
            self.intensity_slider.setValue(85)

        # 确定按钮
        self.setting_ok_button = QPushButton(self)
        self.setting_ok_button.setText("保存")
        self.none_label = QLabel(self)
        self.none_label.setText("            ")
        self.formLayout2.addRow(self.setting_ok_button, self.none_label)

        # 设置连接信号槽函数
        self.intensity_slider.valueChanged.connect(self.valueChange)
        self.intensity_slider.sliderMoved.connect(self.valueChange)
        self.setting_ok_button.clicked.connect(self.confirmChange)

        # 在系统托盘处显示图标
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon('pic/project1.0.ico'))

        # 设置系统托盘图标的菜单
        # 设定显示和退出两个选项
        self.op1 = QAction('&显示(Show)', triggered=self.show)
        self.op2 = QAction('&退出(Exit)', triggered=self.quitApp)

        # 创建菜单并添加选项
        self.trayMenu = QMenu()
        self.trayMenu.addAction(self.op1)
        self.trayMenu.addAction(self.op2)
        self.tray.setContextMenu(self.trayMenu)

        # 设置后台运行时的提示信息
        self.tray.showMessage('圆桌清道夫', '已在后台运行', icon=0)
        # 鼠标双击点击或左键单击点击会唤出主界面
        self.tray.activated.connect(self.act)
    # 槽函数，改变过滤强度标签的值
    def valueChange(self):
        # 获取滑块位置并更改当前过滤强度label
        # 低强度:1-33，中强度:34-66，高强度:67-100
        slider_value = self.intensity_slider.value()
        if (slider_value >= 1 and slider_value <= 33):
            self.final_intensity_label.setText("低强度")
        elif (slider_value >= 34 and slider_value <= 66):
            self.final_intensity_label.setText("中强度")
        else:
            self.final_intensity_label.setText("高强度")

    # 槽函数，确认设置界面中的修改
    def confirmChange(self):
        # 弹窗
        re1 = QMessageBox.question(self, "提示", '确认要修改吗？', QMessageBox.Yes | QMessageBox.No)
        # 确认修改
        if re1 == QMessageBox.Yes:
            # 获取用户设置的强度
            intensity = self.final_intensity_label.text()
            # 修改本地过滤强度
            temp = Setting_Operations()
            result = temp.setIntensity(intensity) # 判断是否修改成功
            if(result):
                re2 = QMessageBox.question(self, "提示", "修改成功！", QMessageBox.Yes)
                # 这里向逻辑线程传递改变过滤强度的信息

            else:
                r2 = QMessageBox.question(self, "提示", "修改失败！请重试", QMessageBox.Yes)
    # 切换至主界面
    def Shift_Main(self):
        self.FilterFrame.setVisible(False)
        self.SettingFrame.setVisible(False)
        self.Message_Receive.setVisible(True)

    # 切换至过滤器界面
    def Shift_Filter(self):
        self.FilterFrame.setVisible(True)
        self.SettingFrame.setVisible(False)
        self.Message_Receive.setVisible(False)

    # 切换至设置界面
    def Shift_Setting(self):
        self.FilterFrame.setVisible(False)
        self.SettingFrame.setVisible(True)
        self.Message_Receive.setVisible(False)
        fliterlist=LoginAndGetMail2_6.showRuleList()
        self.Message_Filter = QLabel(self)
        self.Message_Filter.setText(fliterlist[0])
        self.formLayout2.addRow(self.Message_Filter)

    # 退出程序
    def quitApp(self):
        self.show()  # w.hide() #隐藏
        re = QMessageBox.question(self, "提示", "退出系统", QMessageBox.Yes |
                                  QMessageBox.No, QMessageBox.No)
        if re == QMessageBox.Yes:
            # 关闭窗体程序
            QCoreApplication.instance().quit()
            # 在应用程序全部关闭后，TrayIcon其实还不会自动消失，
            # 直到你的鼠标移动到上面去后，才会消失，
            # 这是个问题，（如同你terminate一些带TrayIcon的应用程序时出现的状况），
            # 这种问题的解决我是通过在程序退出前将其setVisible(False)来完成的。
            self.tray.setVisible(False)

    def act(self, reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            self.show()

    def mousePressEvent(self, event):
        # 判断点击时鼠标不在控件上
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            # 当前鼠标按下的即是QWidget而非界面上布局的其他控件
            self.isPressedWidget = True

    def mouseMoveEvent(self, QMouseEvent):
        # 当前鼠标按下的是QWidget而非界面上布局的其他控件
        if self.isPressedWidget:
            if Qt.LeftButton and self.m_flag:
                self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
                QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.isPressedWidget = False



    # message[0][0][0][2]为发件人，message[0][0][1]为信件内容，message[0][1]为处理结果
    def email_receive(self, Msg):
        msg = eval(Msg)
        # print(msg)
        for message in msg:
            # print(message)
            # print(self.item1)
            # self.addresser = ''.join(message[0][0][0][2])
            # self.content = ''.join(message[0][0][1])
            # self.result = ''.join(message[0][1])
            #在此处获取邮件的发送人
            sender=message[0][0][1]
            #在此处获取邮件的主体
            content=message[0][1]
            #尽可能的去掉邮件主体内部含有的换行符之类
            content = re.sub('\n', '', content)
            content = re.sub('\r','',content)
            content = content.strip()
            #在这里获取邮件对应的判断结果
            reslut=message[1]
            #处理邮件内容，截取前三十字
            len_content = len(content)
            if (len_content >= 20):
                content = content[0:20]
                print(content)
            elif len_content==0:
                content='内容无法显示'
            #格式化输出所得到的结果
            tplt = "{0:{3}^30}\t{1:{3}^20}\t{2:{3}^20}"
            # print(tplt.format(sender,content,reslut,chr(12288)))m
            #将格式化之后的结果添加到显示列表中
            self.item1.append(tplt.format(sender,content,reslut,chr(12288)))
        #显示显示列表内的内容
        self.listmodel1.setStringList(self.item1)
        self.listview1.setModel(self.listmodel1)







