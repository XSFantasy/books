# -*- coding: utf-8 -*-
import os
'''
调用豆瓣API查询图书信息
因为python2.x编码问题，请将此py文件放在IDE中运行
运行此程序前请先在当前目录下创建downloads文件夹
'''
import sys
import urllib
import json
from PyQt4 import QtCore, QtGui
# 豆瓣api利用关键词查询信息
URL = "https://api.douban.com/v2/book/search?q="

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1187, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1187, 600))
        MainWindow.setMaximumSize(QtCore.QSize(1187, 600))
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icon.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(30, 20, 441, 31))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(500, 20, 61, 31))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        
        self.img = QtGui.QLabel(self.centralwidget)
        self.img.setGeometry(QtCore.QRect(30, 90, 181, 251))
        self.img.setObjectName(_fromUtf8("img"))
        
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 60, 1111, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        
        self.bookprofile = QtGui.QTextEdit(self.centralwidget)
        self.bookprofile.setGeometry(QtCore.QRect(340, 90, 731, 251))
        self.bookprofile.setReadOnly(True)
        self.bookprofile.setObjectName(_fromUtf8("bookprofile"))
        
        self.authorprofile = QtGui.QTextEdit(self.centralwidget)
        self.authorprofile.setGeometry(QtCore.QRect(30, 390, 1041, 181))
        self.authorprofile.setReadOnly(True)
        self.authorprofile.setObjectName(_fromUtf8("authorprofile"))
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "图书查询", None))
        self.pushButton.setText(_translate("MainWindow", "找书", None))

class MyWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.goSearch)
        self.myThread = MyThread()
        self.connect(self.myThread, QtCore.SIGNAL(_fromUtf8("done(QString)")), self.display)
        
    def goSearch(self):
        q = str(self.textEdit.toPlainText()).strip()
        self.myThread.q = q
        self.myThread.start()
    
    def display(self, p):
        #set text
        self.authorprofile.setText(self.myThread.author_intro)
        self.bookprofile.setText(self.myThread.summary)
        self.img.setPixmap(QtGui.QPixmap(p))

class MyThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        
        self.summary = None
        self.author_intro = None
        self.q = ''
        self.img_path = '.\\downloads\\'

    def run(self):
        #请求数据
        a = urllib.urlopen(URL+self.q)
        data = a.read()
        b = json.loads(data)
        book = b['books'][0]
        
        self.summary =  book['summary']
        self.author_intro = book['author_intro']
        
        p = self.downloading(book['image'])
        self.emit(QtCore.SIGNAL(_fromUtf8("done(QString)")), p)
        
    def downloading(self, url):
        url_open = urllib.urlopen(url)
        img_data_read = url_open.read(8192)
        img_save = open(self.img_path+os.path.basename(url), "wb")
        while img_data_read:
            
            img_save.write(img_data_read)
            img_data_read = url_open.read(8192)
        img_save.close()
        return self.img_path+os.path.basename(url)
        
app = QtGui.QApplication(sys.argv)
mw = MyWindow(Ui_MainWindow)
mw.show()
sys.exit(app.exec_())        
        
        
