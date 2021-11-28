"""
Create-Date: 2021/11/11
Author:Cunfu Peng
Last-Edit-Date: 2021/11
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import qtawesome
from core import set

# 导航栏
class Nav:
    def __init__(self, parent):

        self.parent = parent

        self.frame()
        self.style()
        self.event()

    def frame(self):

        self.nav = QtWidgets.QLabel(self.parent)
        self.nav.setGeometry(0, 0, 100, 788)

        x = 0
        y = 52
        w = 100
        h = 52

        # 导航栏 发现
        self.found = QtWidgets.QPushButton(" 发现", self.nav)
        self.found.setGeometry(x, y * 0, w, h)
        style_icon = qtawesome.icon("fa5s.search", color=set.NAV_ICON_COLOR)  # 搜索
        self.found.setIcon(style_icon)

        # 导航栏 下载
        self.download = QtWidgets.QPushButton(" 下载", self.nav)
        self.download.setGeometry(x, y * 1, w, h)
        style_icon = qtawesome.icon("fa5s.bars", color=set.NAV_ICON_COLOR)  # 下载
        self.download.setIcon(style_icon)

        # 导航栏 列表
        self.list = QtWidgets.QPushButton(" 列表", self.nav)
        self.list.setGeometry(x, y * 2, w, h)
        style_icon = qtawesome.icon("fa5s.file", color=set.NAV_ICON_COLOR)  # 列表
        self.list.setIcon(style_icon)

        # 导航栏 本地
        self.native = QtWidgets.QPushButton(" 本地", self.nav)
        self.native.setGeometry(x, y * 3, w, h)
        style_icon = qtawesome.icon("fa5s.arrow-circle-down", color="black")  # 本地
        self.native.setIcon(style_icon)

        # 导航栏 设置
        self.set = QtWidgets.QPushButton(" 设置", self.nav)
        self.set.setGeometry(x, y * 4, w, h)
        style_icon = qtawesome.icon("fa5s.cog", color=set.NAV_ICON_COLOR)  # 设置
        self.set.setIcon(style_icon)

        del x, y, w, h

    def event(self):
        self.found.clicked.connect(lambda: self.set_index_style(0))
        self.download.clicked.connect(lambda: self.set_index_style(1))
        self.list.clicked.connect(lambda: self.set_index_style(2))
        self.native.clicked.connect(lambda: self.set_index_style(3))
        self.set.clicked.connect(lambda: self.set_index_style(4))

    def set_index_style(self, n: int):
        self.parent.center.tab.setCurrentIndex(n)
        stylesheet = """
        QPushButton{
            border:none;
            color:black;
            font-size:18px;
            background-color:#eee;
            height:155px;
            font-family:"微软雅黑";
        }
        QPushButton:hover{
            background-color:#ccc;
        }"""
        stylesheet_focus = """
        QPushButton{
            border:none;
            color:black;
            font-size:18px;
            background-color:#ccc;
            height:155px;
            font-family:"微软雅黑";
        }
        QPushButton:hover{
            background-color:#ccc;
        }"""

        self.found.setStyleSheet(stylesheet)
        self.download.setStyleSheet(stylesheet)
        self.list.setStyleSheet(stylesheet)
        self.native.setStyleSheet(stylesheet)
        self.set.setStyleSheet(stylesheet)

        if n == 0:
            self.found.setStyleSheet(stylesheet_focus)
        elif n == 1:
            self.download.setStyleSheet(stylesheet_focus)
        elif n == 2:
            self.list.setStyleSheet(stylesheet_focus)
        elif n == 3:
            self.native.setStyleSheet(stylesheet_focus)
        elif n == 4:
            self.set.setStyleSheet(stylesheet_focus)
        else:
            pass

    def style(self):
        self.nav.setStyleSheet(
            """
            QLabel { 
                background-color:#eee;
            }
            QPushButton { 
                border:none;
                color:black;
                font-size:18px;
                background-color:#eee;
                height:155px;
                font-family:"微软雅黑";
            }
            QPushButton:hover { 
                background-color:#ccc;
            }
            """
        )
