from PyQt5 import QtWidgets, QtCore
from blackDialogUi import Ui_Dialog
import sys
from PyQt5.QtCore import *
import time
import win32clipboard
from AesUtil import decrypt
 

 
# 继承QThread
class Runthread(QtCore.QThread):
    # python3,pyqt5与之前的版本有些不一样
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)
 
    def __init__(self):
        super(Runthread, self).__init__()
 
    def __del__(self):
        self.wait()

    def run(self):
        while(True):
            data = ''
            strDecrypted= ''
            try:
                win32clipboard.OpenClipboard()
                data = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                data=data.strip().replace('\r\n',' ').replace('\r',' ').replace('\n',' ')
                strDecrypted = decrypt(data)
                strDecrypted = str(strDecrypted, 'utf8')  # b转字符串

                pass 
            except Exception as e:
                print(e)
                pass
            
            if strDecrypted != '':
                self._signal.emit(strDecrypted); # 信号发送
                tmpData = strDecrypted
            time.sleep(1)
                


 
class TestQtFromC(QtWidgets.QWidget, Ui_Dialog):
    text =""


    def __init__(self):
        super(TestQtFromC, self).__init__()
        self.setupUi(self)
        self.thread = Runthread() # 创建线程
        self.thread._signal.connect(self.callbacklog) # 连接信号
        self.thread.start() # 开始线程
    #click
    def timer_click(self):
        self.thread = Runthread() # 创建线程
        self.thread._signal.connect(self.callbacklog) # 连接信号
        self.thread.start() # 开始线程
 
    # callback
    def callbacklog(self, msg):
        self.text =msg
        print(self.text)
        # 回调数据输出到文本框
        self.label.setText(self.text);

    def dialogExit(self):
        self.thread.terminate()
        self.thread.quit()
        self.close()
 
 
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     mTestQtFromC = TestQtFromC()
#     mTestQtFromC.show()
#     sys.exit(app.exec_())