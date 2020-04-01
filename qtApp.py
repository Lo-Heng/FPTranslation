import subprocess
import sys
import threading
# from system_hotkey import SystemHotkey
# from pynput.keyboard import Controller, Key, Listener
# import win32clipboard as w
# import win32con
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QKeySequence, QMovie, QPixmap
from PyQt5.QtWidgets import *
from AesUtil import *
from ImgEncryptUtil import *

version = "0.1 alpha"
enFromImgPath = "./enIn.png" # 加密图片默认输入路径
deFromImgPath = "./deIn.bmp" # 解密图片默认输入路径
enToImgPath = "./cache/enOut.bmp"  # 加密图片默认输出路径
deToImgPath = "./cache/deOut.bmp"  # 解密图片默认输出路径
platform = "windows"
winHeigh = 600
winWidth = 800
# class clickBoard():
def getClipImg():
    img = ImageGrab.grabclipboard()
    # img.save('./cache/in.bmp', 'BMP') # 存本地

    # image = QImage('cache/in.png');  
    # self.label.setPixmap(QPixmap.fromImage(img))
    # img.save('paste.bmp', 'BMP')

class panel(QWidget):

    # sig_keyhot = pyqtSignal(str)
    # # def __init__(self,window):
    # #     super().__init__(window)
    # #     #2. 设置我们的自定义热键响应函数
    # #     self.sig_keyhot.connect(self.MKey_pressEvent)
    # #     #3. 初始化两个热键
    # #     self.hk_start,self.hk_stop = SystemHotkey(),SystemHotkey()
    # #     #4. 绑定快捷键和对应的信号发送函数
    # #     self.hk_start.register(('alt','c'),callback=lambda x:self.send_key_event("start"))
    # #     self.hk_stop.register(('alt', 'v'), callback=lambda x: self.send_key_event("stop"))

    # #热键处理函数
    # def MKey_pressEvent(self,i_str):
    #     print("按下的按键是%s" % (i_str))
        
    # #热键信号发送函数(将外部信号，转化成qt信号)
    # def send_key_event(self,i_str):
    #     self.sig_keyhot.emit(i_str)
    def hideLoading(self):
        self.movie.stop()
        self.gifLabel.hide()

    def showLoading(self):
        self.movie.start()
        self.gifLabel.show()

    def handleEnBtn(self):
        strEncrypted = self.text.toPlainText()  # 获取文本框中的东西
        fPath = self.text.toPlainText()
        strEncrypted = encrypt(strEncrypted)
        strEncrypted = str(strEncrypted,encoding='utf8')
        print(strEncrypted)
        #  显示并重新更改框高
        strlen = len(strEncrypted)
        # self.text.resize(500,28 * (int(strlen / 60) + 1))
        self.text.setPlainText(strEncrypted)
        self.hideLoading()
        # --分割-- 下方加密图片
        try:
            fPath = fPath.replace('file://','')
            imgEncrypt(fPath,enToImgPath)
            image = QImage(enToImgPath);  
            self.label.setPixmap(QPixmap.fromImage(image))
        except Exception as e:
            print(e)
            self.lbTopTips.setText('加密失败或找不到图片')
            

    def handleDeBtn(self):
        strDecrypted = self.text.toPlainText()  # 获取文本框中的东西
        dPath = self.text.toPlainText() # 获取输入路径
        try:
            strDecrypted = decrypt(strDecrypted)
            strDecrypted = str(strDecrypted,'utf8') # b转字符串
        except Exception as e:
            print(e)
        # self.text.resize(500,28 * (int(strlen / 60) + 1))
        self.text.setPlainText(strDecrypted)
        #---下方是图像的解密---
        try:
            dPath = dPath.replace('file://','')
            print(dPath)
            imgDecrypt(dPath,deToImgPath)
            image = QImage(deToImgPath);  
            self.label.setPixmap(QPixmap.fromImage(image))
        except Exception as e:
            self.lbTopTips.setText('解密失败或找不到图片')

    def openImage(self):
        imgName = QFileDialog.getOpenFileName(window,"打开图片","","ALL(*.*);;Images(*.png *.jpg *.bmp);;")
        imgPath = imgName[0]
        print(imgPath)
        self.text.setPlainText(imgPath)
    

    def setUI(self,window):

        window.resize(winWidth, winHeigh)
        # 窗口标题
        window.setWindowTitle("fp翻译机 " + version) 

        # 新增一个 用于输出 标签控件
        self.label = QtWidgets.QLabel(window)
        self.label.setAcceptDrops(True)
        self.label.setGeometry(QtCore.QRect(60, 200, 300, 300)) # 标签位置 坐标x,y 宽,高
        self.label.setAlignment(Qt.AlignTop) # 自适应大小
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse) # 鼠标可滑动选中
        self.label.installEventFilter(window)
        self.label.setScaledContents(True) # 自适应

        # 新增一个 loading 标签
        self.gifLabel = QtWidgets.QLabel(window);
        self.gifLabel.setGeometry(60, 200, 200, 150);
        self.movie = QMovie("./src/loading.gif");
        self.movie.setScaledSize(QSize(50,50));
        self.gifLabel.setMovie(self.movie);
        self.movie.start()

        # # 新增一个提示标签控件
        self.lbTopTips = QtWidgets.QLabel(window)
        self.lbTopTips.adjustSize() # 自适应大小
        self.lbTopTips.setGeometry(QtCore.QRect(30, 0, 300, 28)) # 标签位置 坐标x,y 宽,高
        self.lbTopTips.setText("图片拖入下方输入框")

        # # 新增一个右边提示标签控件
        self.lbRight = QtWidgets.QLabel(window)
        self.lbRight.setGeometry(QtCore.QRect(winWidth * 2 / 3, winHeigh / 20, 300, winHeigh)) # 标签位置 坐标x,y 宽,高
        # self.lbRight.adjustSize() # 自适应大小
        self.lbRight.setMaximumWidth( winWidth / 3)
        self.lbRight.setWordWrap(True)
        self.lbRight.setAlignment(Qt.AlignTop)
        self.lbRight.setText("使用说明：\n\n1、快捷键 +++++++++++++++++++++++++++++++++++++++++++++++++\n\n2、sdaihsdiashd ")

        # 新增一个文本框控件
        self.text = QtWidgets.QTextEdit(window) 
        self.text.setGeometry(QtCore.QRect(30,30,500,28 * 3)) # 调整文本框的位置大小
        self.text.installEventFilter(window)

        
        #添加加密按钮和单击事件
        self.enBtn = QtWidgets.QPushButton(window)
        self.enBtn.move(50,100)  #设置按钮的位置，x坐标,y坐标   
        self.enBtn.setText("打开图片") #设置按钮的文字   
        self.enBtn.clicked.connect(self.openImage) #为按钮添加单击事件

        #添加加密按钮和单击事件
        self.enBtn = QtWidgets.QPushButton(window)
        self.enBtn.move(150,100)  #设置按钮的位置，x坐标,y坐标   
        self.enBtn.setText("加密") #设置按钮的文字   
        self.enBtn.clicked.connect(self.handleEnBtn) #为按钮添加单击事件

        #添加解密按钮和单击事件
        self.deBtn = QtWidgets.QPushButton(window)
        self.deBtn.move(250,100)  #设置按钮的位置，x坐标,y坐标   
        self.deBtn.setText("解密") #设置按钮的文字
        self.deBtn.clicked.connect(self.handleDeBtn) #为按钮添加单击事件

        #获取剪切板
        txt=getClipboardData()
        # txt=txt.strip().replace('\r\n',' ').replace('\r',' ').replace('\n',' ')
        print(txt)
    
        # 初始化数据
        self.text.setPlainText(txt)
        
        # 注册退出按钮
        self.shortcut = QShortcut(QKeySequence("ESC"),self )
        self.shortcut.activated.connect(appExit)

        # 注册退出按钮
        self.shortcut = QShortcut(QKeySequence("meta+e"),self )
        self.shortcut.activated.connect(appExit)    

        window.show()
        
# app.exec_() 



# def setWinText(aString):
#     w.OpenClipboard()
#     w.EmptyClipboard()
#     w.SetClipboardData(win32con.CF_TEXT, aString)
#     w.CloseClipboard()

def getClipboardData():
    if(platform == 'darwin'): #如果是苹果

        p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
        retcode = p.wait()
        data = p.stdout.read()
        data = str(data,'utf-8')
        #这里的data为bytes类型，之后需要转成utf-8操作
        return data
    # else: # 如果是windows
    #     w.OpenClipboard()
    #     data = w.GetClipboardData(win32con.CF_TEXT)
    #     w.CloseClipboard()
    #     data = str(data,'utf-8')
    #     return data

def setClipboardData(data):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    p.communicate()


# 图像加密处理
def imgEncrypt(fromPath,toPath):
    imgUtils = ImgUtils()
    imgUtils.imgEncrypt(fromPath,toPath)


# 图像解密处理
def imgDecrypt(fromPath,toPath):
    imgUtils = ImgUtils()
    imgUtils.imgDecrypt(fromPath,toPath)

def appExit():
    sys.exit(app.exec_())


if __name__=='__main__': 

    platform = sys.platform

    app = QtWidgets.QApplication(sys.argv)  # 程序实例
    window = QtWidgets.QWidget()
    ui = panel(window)
    ui.setUI(window)
    sys.exit(app.exec_())
    # print(getClipboardData())
    
    # imgEncrypt()
    # imgDecrypt()

    #按下任何按键时，都会调用abc，其中一定会传一个值，就是键盘事件
    # start_listen()
    #创建应用程序和对象

    # t1.join()
