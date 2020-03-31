from PyQt5.QtWidgets import *
import sys
from PyQt5 import *
# import win32clipboard 
# import win32con
import subprocess
from PIL import ImageGrab
from ImgEncryptUtil import *
from PyQt5.QtCore import Qt
from AesUtil import *
from PyQt5.Qt import *

version = "0.1 alpha"
enFromImgPath = "./enIn.png" # 加密图片默认输入路径
deFromImgPath = "./deIn.bmp" # 解密图片默认输入路径
enToImgPath = "./cache/enOut.bmp"  # 加密图片默认输出路径
deToImgPath = "./cache/deOut.bmp"  # 解密图片默认输出路径
platform = "windows"
# class clickBoard():
def getClipImg():
    img = ImageGrab.grabclipboard()
    img.save('./cache/in.bmp', 'BMP') # 存本地

    # image = QImage('cache/in.png');  
    # self.label.setPixmap(QPixmap.fromImage(img))
    # img.save('paste.bmp', 'BMP')

class panel():

    def handleEnBtn(self):
        strEncrypted = self.text.toPlainText()  # 获取文本框中的东西
        # strEncrypted = encrypt(strEncrypted)
        # strEncrypted = str(strEncrypted,encoding='utf8')
        # print(strEncrypted)
        # #  显示并重新更改框高
        # strlen = len(strEncrypted)
        # print((strlen / 60 + 1))
        # self.text.resize(500,28 * (int(strlen / 60) + 1))
        # self.text.setPlainText(strEncrypted)
        # --分割-- 下方加密图片
        try:
            fPath = self.text.toPlainText()
            fPath = fPath.replace('file://','')
            imgEncrypt(fPath,enToImgPath)
            image = QImage(enToImgPath);  
            self.label.setPixmap(QPixmap.fromImage(image))
        except Exception as e:
            self.lbTips.setText('加密失败或找不到图片')
            

    def handleDeBtn(self):
        strDecrypted = self.text.toPlainText()  # 获取文本框中的东西
        # try:
        #     strDecrypted = decrypt(strDecrypted)
        #     strDecrypted = str(strDecrypted,'utf8') # b转字符串
        # except Exception as e:
        #     print(e)
        # strlen = len(strDecrypted)
        # self.text.resize(500,28 * (int(strlen / 60) + 1))
        # self.text.setPlainText(strDecrypted)
        #---下方是图像的解密---
        try:
            dPath = self.text.toPlainText() # 获取输入路径
            dPath = dPath.replace('file://','')
            print(dPath)
            imgDecrypt(dPath,deToImgPath)
            image = QImage(deToImgPath);  
            self.label.setPixmap(QPixmap.fromImage(image))
        except Exception as e:
            self.lbTips.setText('解密失败或找不到图片')

    # def handleEnPicBtn(self):
        # self.tc = self.text.textCursor()
        # pic = QTextImageFormat()
        # pic.setName('cache/in.png')   #图片路径
        # pic.setHeight(500)            #图片高度
        # pic.setWidth(500)             #图片宽度
        # self.text.resize(500,500)
        # self.tc.insertImage(pic)      #插入图片

    def eventFilter(self, obj, event):
        print(123)
        if obj == self.label:
            if event.type() == QEvent.KeyPress and (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return):
                print(123)
                pass
                return False
            elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Backspace:
                print(111)
                return False
                pass
                # getEditStr = self.label.toPlainText()
                # if len(getEditStr) != 0:
                    # if self.edit.toPlainText()[-1] == '\n':
                        # pass
                # return False
            else:
                return False
        else:
            return QWidget.eventFilter(obj, event)

    def openImage(self):
        imgName = QFileDialog.getOpenFileName(window,"打开图片","","ALL(*.*);;Images(*.png *.jpg *.bmp);;")
        imgPath = imgName[0]
        print(imgPath)
        self.text.setPlainText(imgPath)
    
    def setUI(self,window):

        window.resize(800, 600)
        label = QLabel('Hello World!')
        # 窗口标题
        window.setWindowTitle("fp翻译机 " + version) 

        # 新增一个标签控件
        self.label = QtWidgets.QLabel(window)
        # self.label.adjustSize() # 自适应大小
        self.label.setAcceptDrops(True)
        self.label.setGeometry(QtCore.QRect(60, 200, 300, 300)) # 标签位置 坐标x,y 宽,高
        self.label.setAlignment(Qt.AlignTop) # 自适应大小
        # image = QImage('/Users/gree-lo/Documents/WorkingArea/40设计/格力+/插件&卡片/A_格力空调/B分体/B分体机/插件页/切图标注/切图/空调语音-点击状态.png');  
        # self.label.setPixmap(QPixmap.fromImage(image))
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse) # 鼠标可滑动选中
        # self.label.setText('把图片拖到下面')
        self.label.installEventFilter(window)
        self.label.setScaledContents(True) # 自适应

        # 新增一个提示标签控件
        self.lbTips = QtWidgets.QLabel(window)
        self.lbTips.adjustSize() # 自适应大小
        self.lbTips.setGeometry(QtCore.QRect(30, 0, 300, 28)) # 标签位置 坐标x,y 宽,高
        self.lbTips.setText("图片拖入下方输入框")

        # 新增一个文本框控件
        self.text = QtWidgets.QTextEdit(window) 
        self.text.setGeometry(QtCore.QRect(30,30,500,28 * 1)) # 调整文本框的位置大小
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
        txt=str(getClipboardData(),'utf-8')
        txt=txt.strip().replace('\r\n',' ').replace('\r',' ').replace('\n',' ')
        # print(txt)
    
        # 初始化数据
        self.text.setPlainText(txt)

        window.show()
        
# app.exec_() 



#获取剪切板内容
# def gettext():
#     win32clipboard.OpenClipboard()
#     data = win32clipboard.GetClipboardData()
#     win32clipboard.CloseClipboard()
#     return t

def getClipboardData():
    if(platform == 'darwin'): #如果是苹果

        p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
        retcode = p.wait()
        data = p.stdout.read()
        #这里的data为bytes类型，之后需要转成utf-8操作
        return data
    else: # 如果是windows
        return "dk"

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


if __name__=='__main__': 

    
    # print(getClipboardData())
    
    # imgEncrypt()
    # imgDecrypt()

    platform = sys.platform
    #创建应用程序和对象
    app = QtWidgets.QApplication(sys.argv)  # 程序实例
    window = QtWidgets.QWidget()
    ui = panel()
    ui.setUI(window)
    sys.exit(app.exec_())
