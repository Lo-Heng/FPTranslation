import subprocess
import sys
import threading
from system_hotkey import SystemHotkey
# from pynput.keyboard import Controller, Key, Listener
import win32clipboard as w
import win32con
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QKeySequence, QMovie, QPixmap
from PyQt5.QtWidgets import *
from AesUtil import *
from ImgEncryptUtil import *
from KeyboardUtil import *
from qtTransDIalog import TestQtFromC
import pyperclip
import time
import os

version = "0.1 alpha"
enFromImgPath = "./enIn.png"  # 加密图片默认输入路径
deFromImgPath = "./deIn.bmp"  # 解密图片默认输入路径
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

    sig_keyhot = pyqtSignal(str)

    def __init__(self, window):
        super().__init__(window)
        # 2. 设置我们的自定义热键响应函数
        self.sig_keyhot.connect(self.MKey_pressEvent)
        # 3. 初始化两个热键
        self.hk_start, self.hk_stop = SystemHotkey(), SystemHotkey()
        # 4. 绑定快捷键和对应的信号发送函数
        self.hk_start.register(
            ('alt', 'c'), callback=lambda x: self.send_key_event("enText"))
        self.hk_stop.register(
            ('alt', 'v'), callback=lambda x: self.send_key_event("deText"))

    # 热键处理函数
    def MKey_pressEvent(self, i_str):
        print("按下的按键是%s" % (i_str))
        if(i_str == 'enText'):
            key_up('alt')
            key_up('c')

            # keys_tap(['ctrl', 'a'])

            data = getClipboardData() # 获取剪切板内容
            print (data)
            strEncrypted = encrypt(data)
            strEncrypted = str(strEncrypted, 'utf8')
            print(strEncrypted)

            setClipboardData(strEncrypted)

            keys_tap(['ctrl', 'v'])
        elif (i_str == 'deText'):
            key_up('alt')
            key_up('v')
            # keys_tap(['ctrl', 'a'])
            # keys_tap(['ctrl', 'x'])
            strDecrypted = getClipboardData() # 获取剪切板内容
            
            try:
                strDecrypted = decrypt(strDecrypted)
                strDecrypted = str(strDecrypted, 'utf8')  # b转字符串
            except Exception as e:
                print(e)

            print(strDecrypted)
            setClipboardData(strDecrypted)
            keys_tap(['ctrl', 'v'])

    # 热键信号发送函数(将外部信号，转化成qt信号)
    def send_key_event(self, i_str):
        self.sig_keyhot.emit(i_str)

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
        strEncrypted = str(strEncrypted, encoding='utf8')
        print(strEncrypted)
        #  显示并重新更改框高
        strlen = len(strEncrypted)
        # self.text.resize(500,28 * (int(strlen / 60) + 1))
        self.text.setPlainText(strEncrypted)
        setClipboardData(strEncrypted)
        self.showLoading()
        # --分割-- 下方加密图片
        try:
            self.showLoading()
            fPath = fPath.replace('file://', '')
            imgEncrypt(fPath, enToImgPath)
            image = QImage(enToImgPath)
            self.label.setPixmap(QPixmap.fromImage(image))
        except Exception as e:
            print(e)
            self.lbTopTips.setText('加密失败或找不到图片')

        self.hideLoading()

    def handleDeBtn(self):
        strDecrypted = self.text.toPlainText()  # 获取文本框中的东西
        dPath = self.text.toPlainText()  # 获取输入路径
        try:
            strDecrypted = decrypt(strDecrypted)
            strDecrypted = str(strDecrypted, 'utf8')  # b转字符串
        except Exception as e:
            print(e)
        # self.text.resize(500,28 * (int(strlen / 60) + 1))
        self.text.setPlainText(strDecrypted)
        setClipboardData(strDecrypted)
        self.showLoading()
        # ---下方是图像的解密---
        try:
            dPath = dPath.replace('file://', '')
            print(dPath)
            imgDecrypt(dPath, deToImgPath)
            image = QImage(deToImgPath)
            self.label.setPixmap(QPixmap.fromImage(image))
        except Exception as e:
            self.lbTopTips.setText('解密失败或找不到图片')
        self.hideLoading()
    def openImage(self):
        imgName = QFileDialog.getOpenFileName(
            window, "打开图片", "", "ALL(*.*);;Images(*.png *.jpg *.bmp);;")
        imgPath = imgName[0]
        print(imgPath)
        self.text.setPlainText(imgPath)

    def setUI(self, window):

        window.resize(winWidth, winHeigh)
        # 窗口标题
        window.setWindowTitle("fp翻译机 " + version)
        window.setWindowIcon(QtGui.QIcon('src/logo.png'))
        # 新增一个 用于输出 标签控件
        self.label = QtWidgets.QLabel(window)
        self.label.setAcceptDrops(True)
        self.label.setGeometry(QtCore.QRect(
            winWidth / 2 + 60, 0, winWidth / 2 - 100, winHeigh))  # 标签位置 坐标x,y 宽,高
        self.label.setAlignment(Qt.AlignTop)  # 自适应大小
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # 鼠标可滑动选中
        self.label.installEventFilter(window)
        self.label.setScaledContents(True)  # 自适应

        # 新增一个 loading 标签
        self.gifLabel = QtWidgets.QLabel(window)
        self.gifLabel.setGeometry(winWidth / 6 * 5, winHeigh / 2 ,50, 50) # 标签位置 坐标x,y 宽,高
        self.movie = QMovie("./src/loading.gif")
        self.movie.setScaledSize(QSize(20, 20))
        self.gifLabel.setMovie(self.movie)
        # self.movie.start()
        # self.gifLabel.hide()

        # # 新增一个提示标签控件
        self.lbTopTips = QtWidgets.QLabel(window)
        self.lbTopTips.adjustSize()  # 自适应大小
        self.lbTopTips.setGeometry(QtCore.QRect(
            50, 0, 300, 28))  # 标签位置 坐标x,y 宽,高
        self.lbTopTips.setText("图片或图片拖入下方输入框")

        # # 新增一个右边提示标签控件
        self.lbRight = QtWidgets.QLabel(window)
        self.lbRight.setGeometry(QtCore.QRect(
            50, winHeigh / 2 - 50, winWidth / 2, winHeigh / 2))  # 标签位置 坐标x,y 宽,高
        # self.lbRight.adjustSize() # 自适应大小
        self.lbRight.setMaximumWidth(winWidth / 2)
        self.lbRight.setWordWrap(True)
        self.lbRight.setAlignment(Qt.AlignTop)
        self.lbRight.setText(
            "使用说明：\n\n1、alt + c 将剪贴板内容加密\n   alt + v 将剪贴板内容解密\n\n"
            +"2、图像加解密--加密 点击“打开图片”选择图片-->点击加密，将会输出./cache/enOut.bmp,选择此文件可以发送到微信\n\n"
            +"3、图像加解密--解密 点击“打开图片”选择图片-->点击解密，图片将会输出在此应用中,亦可找到./cache/deOut.bmp查看\n\n"
            +"文字加解密一般用法：ctrl + a ,ctrl + x,alt + c/v \n\n"
            +"图像加解密一般用法：发送方--图片加密过后发送到微信；接收方--收到微信图片右键保存!!--放到本软件解密 ")

        # 新增一个文本框控件
        self.text = QtWidgets.QTextEdit(window)
        self.text.setGeometry(QtCore.QRect(50, 30, winWidth / 2,winHeigh / 4 ))  # 调整文本框的位置大小
        self.text.installEventFilter(window)

        # 添加加密按钮和单击事件
        self.enBtn = QtWidgets.QPushButton(window)
        self.enBtn.move(50, winHeigh / 3)  # 设置按钮的位置，x坐标,y坐标
        self.enBtn.setText("打开图片")  # 设置按钮的文字
        self.enBtn.clicked.connect(self.openImage)  # 为按钮添加单击事件

        # 添加加密按钮和单击事件
        self.enBtn = QtWidgets.QPushButton(window)
        self.enBtn.move(200, winHeigh / 3)  # 设置按钮的位置，x坐标,y坐标
        self.enBtn.setText("加密")  # 设置按钮的文字
        self.enBtn.clicked.connect(self.handleEnBtn)  # 为按钮添加单击事件

        # 添加解密按钮和单击事件
        self.deBtn = QtWidgets.QPushButton(window)
        self.deBtn.move(350, winHeigh / 3)  # 设置按钮的位置，x坐标,y坐标
        self.deBtn.setText("解密")  # 设置按钮的文字
        self.deBtn.clicked.connect(self.handleDeBtn)  # 为按钮添加单击事件

        # 获取剪切板
        # txt = getClipboardData()
        # txt=txt.strip().replace('\r\n',' ').replace('\r',' ').replace('\n',' ')
        # print(txt)

        # 初始化数据
        # self.text.setPlainText(txt)

        # 注册退出按钮
        self.shortcut = QShortcut(QKeySequence("ESC"), self)
        self.shortcut.activated.connect(appExit)

        # 注册退出按钮 MAC
        self.shortcut = QShortcut(QKeySequence("meta+w"), self)
        self.shortcut.activated.connect(appExit)

        window.show()

# app.exec_()


# def setWinText(aString):
#     w.OpenClipboard()
#     w.EmptyClipboard()
#     w.SetClipboardData(win32con.CF_TEXT, aString)
#     w.CloseClipboard()


def getClipboardData():
    data =''
    data = pyperclip.paste()
    # w.OpenClipboard()
    # data = w.GetClipboardData()
    # w.CloseClipboard()
    return data


def setClipboardData(data):
    # os.system("echo off | clip")
    w.OpenClipboard()
    w.EmptyClipboard()
    # w.SetClipboardData(w.CF_TEXT, data)
    w.SetClipboardText( data,w.CF_TEXT  )
    w.CloseClipboard()
# 图像加密处理
def imgEncrypt(fromPath, toPath):
    imgUtils = ImgUtils()
    imgUtils.imgEncrypt(fromPath, toPath)


# 图像解密处理
def imgDecrypt(fromPath, toPath):
    imgUtils = ImgUtils()
    imgUtils.imgDecrypt(fromPath, toPath)


def appExit():
    sys.exit(app.exec_())


if __name__ == '__main__':

    platform = sys.platform

    app = QtWidgets.QApplication(sys.argv)  # 程序实例
    window = QtWidgets.QWidget()
    ui = panel(window)
    ui.setUI(window)
    mTestQtFromC = TestQtFromC()
    mTestQtFromC.show()
    sys.exit(app.exec_())
