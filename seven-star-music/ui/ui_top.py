"""
Create-Date: 2021/11/11
Author:Cunfu Peng
Last-Edit-Date: 2021/11
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from core.music import Netease,Utils
import qtawesome
from core import set


# from ui_main import mainwin

# 顶部区域
class Top:
    def __init__(self, parent):
        self.parent = parent
        self.frame()
        self.style()
        self.event()

    def frame(self):

        self.top = QtWidgets.QLabel(self.parent)
        self.top.setGeometry(100, 0, 1144, 52)

        # 顶部 歌曲源区域 组合框
        self.top_sourcefrom = QtWidgets.QLabel(self.top)
        self.top_sourcefrom.setGeometry(6, 6, 76, 50)
        self.sourcefrom = QtWidgets.QComboBox(self.top_sourcefrom)
        self.sourcefrom.setGeometry(0, 2, 76, 36)
        self.sourcefrom.addItem(" 网易云")
        self.sourcefrom.addItem(" 酷狗")
        self.sourcefrom.addItem(" QQ")
        self.sourcefrom.addItem(" 酷我")
        self.sourcefrom.setCurrentIndex(0)
        # self.sourcefrom.setEnabled(False)

        # == 顶部 搜索区域 ==
        self.top_search = QtWidgets.QLabel(self.top)
        self.top_search.setGeometry(86, 6, 500, 50)

        # 顶部搜索框
        self.searchbox = QtWidgets.QLineEdit(self.top_search)
        self.searchbox.setGeometry(0, 2, 300, 36)
        self.searchbox.setPlaceholderText("Search for something...")

        # 顶部搜索按钮
        self.searchbtn = QtWidgets.QPushButton(self.top_search)
        self.searchbtn.setGeometry(300, 2, 50, 36)
        style_icon = qtawesome.icon("fa5s.search", color=156456)  # 搜索
        self.searchbtn.setIcon(style_icon)

        # == 顶部 控制区域 ==
        self.top_ctrl = QtWidgets.QLabel(self.top)
        self.top_ctrl.setGeometry(1060, 10, 80, 50)

        # 最小化按钮
        self.mini = QtWidgets.QPushButton(self.top_ctrl)
        self.mini.setGeometry(4, 4, 24, 24)
        style_icon = qtawesome.icon("fa5s.minus", color="white")  # 最小化
        self.mini.setIcon(style_icon)

        # 关闭按钮
        self.close = QtWidgets.QPushButton(self.top_ctrl)
        self.close.setGeometry(36, 4, 24, 24)
        style_icon = qtawesome.icon("fa5s.times", color="white")  # 关闭
        self.close.setIcon(style_icon)

    def event(self):
        # 控制按钮
        self.mini.clicked.connect(self.parent.showMinimized)
        self.close.clicked.connect(self.parent.close)

        self.searchbtn.clicked.connect(self.searchMusic)

    def searchMusic(self):
        name = self.searchbox.text()
        if name != "":
            self.parent.center.found.setCurrentIndex(2)
            sch_rsts = Netease.single_search(name)
            self.parent.center.search.setRowCount(sch_rsts.__len__())
            for i in range(0, sch_rsts.__len__()):
                print(sch_rsts[i])
                id = sch_rsts[i]["id"]
                name = sch_rsts[i]["name"]
                alias = sch_rsts[i]["alias"]
                duration = sch_rsts[i]["duration"]

                artists = sch_rsts[i]["artists"]
                artists_id = artists[0]["id"]
                artists_name = artists[0]["name"]

                album = sch_rsts[i]["album"]
                album_id = album["id"]
                album_picId = album["picId"]
                album_name = album["name"]

                self.parent.center.search.setItem(
                    i, 0, QtWidgets.QTableWidgetItem(name)
                )
                self.parent.center.search.setItem(
                    i, 1, QtWidgets.QTableWidgetItem(artists_name)
                )
                self.parent.center.search.setItem(
                    i, 2, QtWidgets.QTableWidgetItem(album_name)
                )
                self.parent.center.search.setItem(
                    i,
                    3,
                    QtWidgets.QTableWidgetItem(Utils.durationToString(duration)),
                )

    def style(self):
        self.top_search.setStyleSheet(
            """
            QLineEdit{ 
                border:none;
                color:black;
                background-color:#ddd;
                font-size:14px;
                font-family:微软雅黑;
                padding-left:8px;
                border-top-left-radius:5px;
                border-bottom-left-radius:5px;
            }
            QPushButton { 
                border:none;
                background-color:#ddd;
                border-top-right-radius:5px;
                border-bottom-right-radius:5px;
            }
            QPushButton:hover { 
                background-color:#ccc;
            }
            """
        )

        self.sourcefrom.setStyleSheet(
            """
            QComboBox{
                border:none;
                font-family:"微软雅黑";
                font-size:12px;
                color:black;
                border-radius:5px;
            }
            
            QComboBox QAbstractItemView{
                border:0;
            }
            
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left-width: 0px;
                border-left-color: gray;
                border-left-style: solid;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
            }
            
            QComboBox::down-arrow {    
                border-image: url(:/image/down.png);
            }
            
            QComboBox::down-arrow:hover {    
                border-image: url(:/image/up.png);

            }
    
            QComboBox::down-arrow:pressed {   
                border-image: url(:/image/up.png);
            }
            """
        )

        self.mini.setStyleSheet(
            """
            QPushButton {
                border:none;
                border-radius:12px;
                background-color:#4caf50;
            } 
            QPushButton:hover { 
                background-color:#388e3c;
            }
            """
        )

        self.close.setStyleSheet(
            """
            QPushButton {
                border:none;
                border-radius:12px;
                background-color:red;
            } 
            QPushButton:hover {
                background-color:rgb(210,0,0);
            }
            """
        )
