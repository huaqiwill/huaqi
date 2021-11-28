"""
Create-Date: 2021/11/11
Author:Cunfu Peng
Last-Edit-Date: 2021/11
"""

import os
import time

from PyQt5 import QtCore, QtGui, QtWidgets

# import qtawesome
import requests
from core.music import Netease
from core.play import Player
from core import set

import _thread


class varname:
    # 歌曲信息  存入 dict
    # {"id":"2003","duration":"02:45",...}
    music_info = []

    # 音乐源
    music_source_lists = {
        "网易云": {
            "热歌榜": "https://music.163.com/discover/toplist?id=3778678",
            "新歌榜": "https://music.163.com/discover/toplist?id=3779629",
            "原创榜": "https://music.163.com/discover/toplist?id=2884035",
            "飙升榜": "https://music.163.com/discover/toplist?id=19723756",
        },
        "酷狗": {
            "飙升榜": "https://www.kugou.com/yy/rank/home/1-6666.html?from=rank",
            "TOP500": "https://www.kugou.com/yy/rank/home/1-8888.html?from=rank",
            "抖音热歌榜": "https://www.kugou.com/yy/rank/home/1-52144.html?from=rank",
            "快手热歌榜": "https://www.kugou.com/yy/rank/home/1-52767.html?from=rank",
            "国风新歌榜": "https://www.kugou.com/yy/rank/home/1-33161.html?from=rank",
            "电音热歌榜": "https://www.kugou.com/yy/rank/home/1-33160.html?from=rank",
            "影视金曲榜": "https://www.kugou.com/yy/rank/home/1-33163.html?from=rank",
        },
        "QQ": {
            "飙升榜": "https://y.qq.com/n/ryqq/toplist/62",
            "热歌榜": "https://y.qq.com/n/ryqq/toplist/26",
            "新歌榜": "https://y.qq.com/n/ryqq/toplist/27",
            "国风热歌榜": "https://y.qq.com/n/ryqq/toplist/65",
        },
        "酷我": {
            "飙升榜": "http://www.kuwo.cn/rankList",
            "热歌榜": "http://www.kuwo.cn/rankList",
            "新歌榜": "http://www.kuwo.cn/rankList",
        },
    }


# from gui.ui_main import mainwin

# 中部区
class Center:
    def __init__(self, parent):
        self.parent = parent

        self.frame()
        self.style()
        self.event()
        self.loading_data()
        

    def frame(self):
        self.center = QtWidgets.QLabel(self.parent)  # [-0-]
        self.center.setGeometry(100, 52, 1144, 660)
        # self.center.setStyleSheet("QLabel{background-color:rgb(209,232,247);}")

        # 发现，下载，列表，本地，下载
        self.tab_found = QtWidgets.QWidget()
        self.tab_download = QtWidgets.QWidget()
        self.tab_playlist = QtWidgets.QWidget()
        self.tab_native = QtWidgets.QWidget()
        self.tab_setting = QtWidgets.QWidget()

        # 中部
        self.tab = QtWidgets.QTabWidget(self.center)  # [-1-]
        self.tab.setGeometry(6, 0, 1129, 660)
        self.tab.tabBar().hide()  # 隐藏表头

        self.tab.addTab(self.tab_found, " 发现")
        self.tab.addTab(self.tab_download, " 下载")
        self.tab.addTab(self.tab_playlist, " 列表")
        self.tab.addTab(self.tab_native, " 本地")
        self.tab.addTab(self.tab_setting, " 设置")

        # 发现
        self.found = QtWidgets.QTabWidget(self.tab_found)  # [-3-]
        self.found.setGeometry(0, 0, 1129, 660)

        # 下载
        self.download = QtWidgets.QTableWidget(self.tab_download)  # [-3-]
        self.download.setGeometry(0, 0, 1129, 648)
        self.download.setColumnCount(4)
        self.download.setHorizontalHeaderLabels(["歌曲名", "歌手", "下载状态", "下载进度"])
        self.download.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.download.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )  # 设置整行选中
        self.download.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed
        )  # 使用户无法调整
        self.download.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.download.setColumnWidth(0, 420)
        self.download.setColumnWidth(1, 180)
        self.download.setColumnWidth(2, 110)
        self.download.setColumnWidth(3, 360)

        # 本地
        self.native = QtWidgets.QTableWidget(self.tab_native)  # [-3-]
        self.native.setGeometry(70, 0, 1029, 630)
        self.native.setColumnCount(3)
        self.native.setHorizontalHeaderLabels(["歌曲名", "时长", "操作"])
        self.native.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.native.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )  # 设置整行选中
        self.native.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed
        )  # 使用户无法调整
        self.native.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.native.setColumnWidth(0, 745)
        self.native.setColumnWidth(1, 105)
        self.native.setColumnWidth(2, 120)

        # 推荐，歌单，搜索
        self.found_recommand = QtWidgets.QWidget()  # [-4-]
        self.found_songlist = QtWidgets.QWidget()  # [-4-]
        self.found_searching = QtWidgets.QWidget()  # [-4-]

        self.found.addTab(self.found_recommand, "推荐")
        self.found.addTab(self.found_songlist, "歌单")
        self.found.addTab(self.found_searching, "搜索")

        w = 80
        h = 80

        # 排行榜 歌单列表
        self.rocking = QtWidgets.QTableWidget(self.found_recommand)  # [-5-]
        self.rocking.setGeometry(0, 0, 262, 630)
        self.rocking.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed
        )  # 固定单元格尺寸
        self.rocking.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.rocking.horizontalHeader().setVisible(False)  # 隐藏水平表头
        self.rocking.verticalScrollBar().setHidden(True)  # 隐藏垂直滚动条
        self.rocking.horizontalScrollBar().setHidden(True)  # 隐藏水平滚动条
        self.rocking.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )  # 设置整行选中
        self.rocking.setColumnCount(1)
        self.rocking.setColumnWidth(0, 255)

        music_source_list = [
            "• 网易云",
            "  热歌榜",
            "  新歌榜",
            "  原创榜",
            "  飙升榜",
            "• 酷狗",
            "  飙升榜",
            "  TOP500",
            "  抖音热歌榜",
            "  快手热歌榜",
            "  国风新歌榜",
            "  电音热歌榜",
            "  影视金曲榜",
            "• QQ",
            "  飙升榜",
            "  热歌榜",
            "  新歌榜",
            "  国风热歌榜",
            "• 酷我",
            "  飙升榜",
            "  热歌榜",
            "  新歌榜",
        ]

        self.rocking.setRowCount(music_source_list.__len__())
        for i in range(0, music_source_list.__len__()):
            self.rocking.setItem(i, 0, QtWidgets.QTableWidgetItem(music_source_list[i]))

        font = QtGui.QFont("微软雅黑", 12)
        self.rocking.item(0, 0).setFont(font)
        self.rocking.item(5, 0).setFont(font)
        self.rocking.item(13, 0).setFont(font)
        self.rocking.item(18, 0).setFont(font)

        # 设置不可选中
        self.rocking.item(0, 0).setFlags(QtCore.Qt.ItemIsSelectable)
        self.rocking.item(5, 0).setFlags(QtCore.Qt.ItemIsSelectable)
        self.rocking.item(13, 0).setFlags(QtCore.Qt.ItemIsSelectable)
        self.rocking.item(18, 0).setFlags(QtCore.Qt.ItemIsSelectable)

        self.rocking.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.rocking.setItem(0,0,QtWidgets.QTableWidgetItem("网易云"))
        # self.rocking.setItem(1,0,QtWidgets.QTableWidgetItem("酷狗"))
        # self.rocking.setItem(2,0,QtWidgets.QTableWidgetItem("酷我"))
        # self.rocking.setItem(3,0,QtWidgets.QTableWidgetItem("QQ"))

        del w, h

        # 音乐信息
        self.songinfo = QtWidgets.QTableWidget(self.found_recommand)  # [-5-]
        self.songinfo.setGeometry(243, 0, 886, 630)
        self.songinfo.setColumnCount(5)
        self.songinfo.setHorizontalHeaderLabels(["歌曲名", "歌手", "时长", "专辑", "操作"])
        self.songinfo.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )  # 设置整行选中
        self.songinfo.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )  # 设置不可编辑
        self.songinfo.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed
        )  # 固定单元格尺
        self.songinfo.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.songinfo.setColumnWidth(0, 320)
        self.songinfo.setColumnWidth(1, 150)
        self.songinfo.setColumnWidth(2, 90)
        self.songinfo.setColumnWidth(3, 150)
        self.songinfo.setColumnWidth(4, 120)

        # 歌单
        self.songlist = QtWidgets.QTableWidget(self.found_songlist)  # [-5-]
        self.songlist.setGeometry(0, 0, 1129, 630)
        # self.songlist.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # 设置整行选中
        self.songlist.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )  # 设置不可编辑
        self.songlist.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed
        )  # 固定单元格尺寸
        self.songlist.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.songlist.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.songlist.horizontalHeader().setVisible(False)  # 隐藏水平表头

        # 搜索
        self.search = QtWidgets.QTableWidget(self.found_searching)  # [-5-]
        self.search.setGeometry(0, 0, 1129, 630)
        self.search.setColumnCount(5)
        self.search.setHorizontalHeaderLabels(["歌曲名", "歌手", "专辑", "时长", "操作"])
        self.search.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.search.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )  # 设置整行选中
        self.search.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed
        )  # 使用户无法调整
        self.search.setColumnWidth(0, 420)
        self.search.setColumnWidth(1, 180)
        self.search.setColumnWidth(2, 260)
        self.search.setColumnWidth(3, 110)
        self.search.setColumnWidth(4, 100)

        self.player = Player(self.parent)
        self.native_base = native_base(self)
        self.playlist_base = playlist_base(self)
        self.setting_base = setting_base(self)

    def event(self):
        self.songinfo.clicked.connect(self.addtoPlaylist)
        self.rocking.clicked.connect(self.rocking_clicked)

    def loading_data(self):

        # ====================================================================
        # 热歌榜

        rst_songlist = Netease.get_recommoned()

        row = rst_songlist.__len__()
        self.songinfo.setRowCount(row)
        self.addOpration(self.songinfo, row, 4)

        for i in range(0, row):

            albumn = rst_songlist[i]["album"]
            artists = rst_songlist[i]["artists"]

            dic_info = {
                "name": rst_songlist[i]["name"],
                "duration": self.durationToString(rst_songlist[i]["duration"]),
                "id": rst_songlist[i]["id"],
                "artists_name": artists[0]["name"],
                "artists_id": artists[0]["id"],
                "albumn_picurl": albumn["picUrl"],
                "albumn_id": albumn["id"],
                "albumn_name": albumn["name"],
            }

            varname.music_info.append(dic_info)

            self.songinfo.setItem(i, 0, QtWidgets.QTableWidgetItem(dic_info["name"]))
            self.songinfo.setItem(
                i, 1, QtWidgets.QTableWidgetItem(dic_info["artists_name"])
            )
            self.songinfo.setItem(
                i, 2, QtWidgets.QTableWidgetItem(dic_info["duration"])
            )
            self.songinfo.setItem(
                i, 3, QtWidgets.QTableWidgetItem(dic_info["albumn_name"])
            )

        # ====================================================================
        # 歌单

        soups = Netease.get_songlist()
        self.songlist.setColumnCount(6)

        for i in range(0, 6):
            self.songlist.setColumnWidth(i, 185)

        self.songlist.setRowCount(int(soups.__len__() / 6) + 1)
        # find,get方法继承来自BeautifulSoup,由方法get_songlist()返回

        for i in range(0, soups.__len__()):
            img = soups[i].find("img")
            name = soups[i].find("a")
            img = img.get("src")
            href = name.get("href")
            title = name.get("title")

            w_pic = QtWidgets.QLabel()
            map = QtGui.QPixmap(130, 130)
            map.loadFromData(requests.get(img).content)
            w_pic.setPixmap(map)

            w_title = QtWidgets.QLabel()
            w_title.setFont(QtGui.QFont("微软雅黑", 10))
            w_title.setText(title)

            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(w_pic)
            layout.addWidget(w_title)

            w_lb = QtWidgets.QLabel(self.songlist)
            w_lb.setLayout(layout)

            a = i % 6
            b = int(i / 6)
            self.songlist.setCellWidget(b, a, w_lb)

            # self.songlist.setItem(i,1,QtWidgets.QTableWidgetItem(href))
            # self.songlist.setItem(i,2,QtWidgets.QTableWidgetItem(img))

            self.songlist.setRowHeight(i, 185)

    def durationToString(self, duration: int):
        duration = int(duration / 1000)
        sec = duration % 60
        min = int((duration - sec) / 60)
        sec = "00" + str(sec)
        min = "00" + str(min)
        sec = sec[sec.__len__() - 2 :]
        min = min[min.__len__() - 2 :]
        return min + ":" + sec

    def addtoPlaylist(self):
        row = self.songinfo.currentRow()

        title = self.songinfo.item(row, 0).text()
        artist = self.songinfo.item(row, 1).text()
        duration = self.songinfo.item(row, 2).text()
        album = self.songinfo.item(row, 3).text()

        title = varname.music_info[row]["name"]
        artist = varname.music_info[row]["artists_name"]

        if set.IS_DEBUG:
            print(title, artist, duration, album)

        row = self.playlist_base.right_list.rowCount()

        self.playlist_base.right_list.setRowCount(row + 1)
        self.playlist_base.right_list.setItem(row, 0, QtWidgets.QTableWidgetItem(title))
        self.playlist_base.right_list.setItem(
            row, 1, QtWidgets.QTableWidgetItem(artist)
        )
        self.playlist_base.right_list.setItem(row, 2, QtWidgets.QTableWidgetItem(album))
        self.playlist_base.right_list.setItem(
            row, 3, QtWidgets.QTableWidgetItem(duration)
        )

        id = varname.music_info[row]["id"]
        picUrl = varname.music_info[row]["albumn_picurl"]
        url = Netease.get_musicUrl_byId(id)

        if set.IS_DEBUG:
            print(id)
            print(url)

        self.player.play(url, "url", 100)

        map = QtGui.QPixmap(75, 75)
        map.loadFromData(requests.get(picUrl).content)
        self.parent.bottom.info_pic.setPixmap(map.scaledToWidth(75))
        self.parent.bottom.info_pic.setPixmap(map.scaledToHeight(75))

        self.parent.bottom.info_title.setText(title + " - " + artist)
        self.parent.bottom.info_time_2.setText(duration)
        self.parent.bottom.info_time_1.setText("00:00")

        # self.time_count_duration = 0

        # _thread.start_new_thread(self.durationAdd)

    # def durationAdd(self):
    #     self.time_count_duration += 1000;
    #     duration = netease.net_music.durationToString(self.time_count_duration)
    #     self.parent.bottom.info_time_1.setText(duration)
    #     # time.sleep(1000)
    #     print(1)
    #     self.durationAdd()

    def rocking_clicked(self):
        index = self.rocking.currentRow()
        if set.IS_DEBUG:
            print("rocking - 点击:" + str(index))

        if index == 0 or index == 5 or index == 13 or index == 18:
            return

        if index == 1:
            if set.IS_DEBUG:
                print("网易 - 热歌榜 - 1")
            # CODE
            rst_songlist = Netease.get_recommoned(
                varname.music_source_lists["网易云"]["热歌榜"]
            )
            self.set_songinfo_content(rst_songlist)
            return

        if index == 2:
            if set.IS_DEBUG:
                print("网易 - 新歌榜 - 2")
            # CODE
            rst_songlist = Netease.get_recommoned(
                varname.music_source_lists["网易云"]["新歌榜"]
            )
            self.set_songinfo_content(rst_songlist)
            return

        if index == 3:
            if set.IS_DEBUG:
                print("网易 - 原创榜 - 3")
            # CODE
            rst_songlist = Netease.get_recommoned(
                varname.music_source_lists["网易云"]["原创榜"]
            )
            self.set_songinfo_content(rst_songlist)
            return

        if index == 4:
            if set.IS_DEBUG:
                print("网易 - 飙升榜 - 4")
            # CODE
            rst_songlist = Netease.get_recommoned(
                varname.music_source_lists["网易云"]["飙升榜"]
            )
            self.set_songinfo_content(rst_songlist)
            return

        if index == 6:
            if set.IS_DEBUG:
                print("酷狗 - 1")
            # CODE

            return
        if index == 7:
            if set.IS_DEBUG:
                print("酷狗 - 2")
            # CODE

            return
        if index == 8:
            if set.IS_DEBUG:
                print("酷狗 - 3")
            # CODE

            return

        if index == 9:
            if set.IS_DEBUG:
                print("酷狗 - 4")
            # CODE

            return

        if index == 10:
            if set.IS_DEBUG:
                print("酷狗 - 5")
            # CODE

            return
        if index == 11:
            if set.IS_DEBUG:
                print("酷狗 - 6")
            # CODE

            return

        if index == 12:
            if set.IS_DEBUG:
                print("酷狗 - 7")
            # CODE

            return
        if index == 14:
            if set.IS_DEBUG:
                print("QQ - 1")
            # CODE

            return

        if index == 15:
            if set.IS_DEBUG:
                print("QQ - 2")
            # CODE

            return

        if index == 16:
            if set.IS_DEBUG:
                print("QQ - 3")
            # CODE

            return

        if index == 17:
            if set.IS_DEBUG:
                print("QQ - 4")
            # CODE

            return

        if index == 19:
            if set.IS_DEBUG:
                print("酷我 - 1")
            # CODE

            return

        if index == 20:
            if set.IS_DEBUG:
                print("酷我 - 2")
            # CODE

            return

        if index == 21:
            if set.IS_DEBUG:
                print("酷我 - 3")
            # CODE

            return

    def set_songinfo_content(self, rst_songlist: list):
        row = rst_songlist.__len__()

        self.songinfo.setRowCount(row)
        self.addOpration(self.songinfo, row)

        for i in range(0, row):
            albumn = rst_songlist[i]["album"]
            artists = rst_songlist[i]["artists"]

            dic_info = {
                "name": rst_songlist[i]["name"],
                "duration": self.durationToString(rst_songlist[i]["duration"]),
                "id": rst_songlist[i]["id"],
                "artists_name": artists[0]["name"],
                "artists_id": artists[0]["id"],
                "albumn_picurl": albumn["picUrl"],
                "albumn_id": albumn["id"],
                "albumn_name": albumn["name"],
            }

            self.songinfo.setItem(i, 0, QtWidgets.QTableWidgetItem(dic_info["name"]))
            self.songinfo.setItem(
                i, 1, QtWidgets.QTableWidgetItem(dic_info["artists_name"])
            )
            self.songinfo.setItem(
                i, 2, QtWidgets.QTableWidgetItem(dic_info["duration"])
            )
            self.songinfo.setItem(
                i, 3, QtWidgets.QTableWidgetItem(dic_info["albumn_name"])
            )

    def addOpration(self, parent, row: int, column: int):

        for i in range(0, row):
            la = QtWidgets.QLabel()
            ctrl_1 = QtWidgets.QPushButton(la)
            ctrl_1.setGeometry(0, 0, 30, 30)

            ctrl_2 = QtWidgets.QPushButton(la)
            ctrl_2.setGeometry(30, 0, 30, 30)

            ctrl_3 = QtWidgets.QPushButton(la)
            ctrl_3.setGeometry(60, 0, 30, 30)

            self.songinfo.setCellWidget(i, column, la)

            # event
            ctrl_1.clicked.connect(lambda: self.ctrl_1_play(i))
            ctrl_2.clicked.connect(lambda: self.ctrl_2_play(i))
            ctrl_3.clicked.connect(lambda: self.ctrl_3_play(i))
            # style

    def ctrl_1_play(self, n: int):
        row = self.songinfo.currentRow()
        if set.IS_DEBUG:
            print("songinfo - ctrl-1-play - " + str(n))
        pass

    def ctrl_2_play(self, n: int):
        row = self.songinfo.currentRow()
        if set.IS_DEBUG:
            print("songinfo - ctrl-2-play - " + str(n))
        pass

    def ctrl_3_play(self, n: int):
        row = self.songinfo.currentRow()
        if set.IS_DEBUG:
            print("songinfo - ctrl-3-play - " + str(n))
        pass

    def style(self):
        self.tab.setStyleSheet(
            """
            QTabWidget{ 
                border:none;
                font-size:16px;
                font-family:"微软雅黑";
            }
            """
        )

        self.native.setStyleSheet(
            """
            QTableView,QTabWidget::pane {
                border:none;
                selection-background-color:rgb(52,152,200);
                selection-color:#40E0D0;
                alternate-background-color:#525252;
                gridline-color:#fff;
            }
            """
        )

        self.rocking.setStyleSheet(
            """
            QTableWidget{
                border:none;
                gridline-color:#fff;
            }
            """
        )

        self.songinfo.setStyleSheet(
            """
            QTableView,QTabWidget::pane{ 
                border:none;
                selection-background-color:rgb(52,152,200);
                selection-color:white;
                alternate-background-color:#505050;
                gridline-color:#fff;
            }"""
        )

        # ========================================
        # Qss界面美化3：QTableWidget美化
        # https://blog.csdn.net/parkchorong/article/details/102661052

        self.rocking.setStyleSheet(
            """
            /*tabelwidget*/
            QTableWidget{
                color:#000;
                background:#fff;
                border:0;
                /*alternate-background-color:#525252;*//*交错颜色*/
                /*gridline-color:#242424;*/
            }
    
            /*选中item*/
            QTableWidget::item:selected{
                color:#fff;
                /*background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #484848,stop:1 #383838);*/
    
                background-color:#666;
            }
    
            /*悬浮item*/
            QTableWidget::item:hover{
                /*background:#5B5B5B;*/
            }
    
            /*表头*/
            QHeaderView::section{
                text-align:center;
                background:#5E5E5E;
                padding:3px;
                margin:0px;
                color:#DCDCDC;
                border:1px solid #242424;
                border-left-width:0;
            }
    
            /*表右侧的滑条*/
            QScrollBar:vertical{
                background:#484848;
                padding:0px;
                border-radius:6px;
                max-width:12px;
            }
    
            /*滑块*/
            QScrollBar::handle:vertical{
                background:#CCCCCC;
                }
                /*
                滑块悬浮，按下*/
                QScrollBar::handle:hover:vertical,QScrollBar::handle:pressed:vertical{
                background:#A7A7A7;
                }
                /*
                滑块已经划过的区域*/
                QScrollBar::sub-page:vertical{
                background:444444;
            }
    
            /*
            滑块还没有划过的区域*/
            QScrollBar::add-page:vertical{
                background:5B5B5B;
            }
    
            /*页面下移的按钮*/
            QScrollBar::add-line:vertical{
                background:none;
            }
    
            /*页面上移的按钮*/
            QScrollBar::sub-line:vertical{
                background:none;
            }
            """
        )
        # ========================================

        self.search.setStyleSheet(
            """
            QTableWidget{
                color:#000;
                background:#fff;
                border:0;
            }

            /*选中item*/
            QTableWidget::item:selected{
                color:#fff;
                background-color:rgb(36,172,242);
            }

            /*悬浮item*/
            QTableWidget::item:hover{
                
            }
            """
        )

        self.songlist.setStyleSheet(
            """
            QTableWidget{
            color:#000;
            background:#fff;
            border:0;
            }

            /*选中item*/
            QTableWidget::item:selected{
                color:#fff;
                background-color:#eee;
                border:0;
                outline:0;
            }

            /*悬浮item*/
            QTableWidget::item:hover{
                
            }
            """
        )


# from ui_main import mainwin


class native_base:
    def __init__(self, parent):
        self.parent = parent

        self.browser_btn = QtWidgets.QPushButton(parent.tab_native)
        self.browser_btn.setText("浏览")
        self.browser_btn.setGeometry(0, 30, 60, 30)

        self.open_btn = QtWidgets.QPushButton(parent.tab_native)
        self.open_btn.setText("添加")
        self.open_btn.setGeometry(0, 60, 60, 30)

        self.delete_btn = QtWidgets.QPushButton(parent.tab_native)
        self.delete_btn.setText("删除")
        self.delete_btn.setGeometry(0, 90, 60, 30)

        self.style()
        self.event()

    def event(self):
        self.browser_btn.clicked.connect(lambda: self.browser_clicked())
        self.open_btn.clicked.connect(lambda: self.open_clicked())
        self.delete_btn.clicked.connect(lambda: self.delete_clicked())

    def browser_clicked(self):
        print("浏览")
        # 选择文件夹 对话框
        dir = QtWidgets.QFileDialog.getExistingDirectory(
            self.parent.parent, "请选择包含音乐的文件夹："
        )
        files = self.EnumFiles(dir)
        for file in files:
            print(file)

    def open_clicked(self):
        print("添加")
        # 文件另存为
        # 对话框
        # QFileDialog.getSaveFileName()

        # 文件另存为
        # 对话框
        #
        # QFileDialog.getSaveFileName()

        # 选择文件 对话框
        file_name = QtWidgets.QFileDialog.getOpenFileName(
            self.parent.parent, "选取音频文件", os.getcwd(), "mp3文件(*.mp3);;所有文件(*.*)"
        )[0]
        print(file_name)

    def delete_clicked(self):
        print("删除")

    # 枚举文件
    def EnumFiles(self, path: str, isPath: bool = True):
        files = os.listdir(path)
        if isPath:
            for i in range(0, files.__len__()):
                files[i] = path + "/" + files[i]
        return files

    def style(self):
        self.browser_btn.setStyleSheet(
            """
            QPushButton{
                border:0;
                background-color:rgb(10,133,217);
                color:white;
            }

            QPushButton:hover{
                background-color:rgb(77,210,168);
            }
            """
        )

        self.open_btn.setStyleSheet(
            """
            QPushButton{
                border:0;
                background-color:rgb(10,133,217);
                color:white;
            }

            QPushButton:hover{
                background-color:rgb(77,210,168);
            }

            """
        )

        self.delete_btn.setStyleSheet(
            """
            QPushButton{
                border:0;
                background-color:rgb(10,133,217);
                color:white;
            }

            QPushButton:hover{
                background-color:rgb(77,210,168);
            }
            """
        )


class playlist_base:
    def __init__(self, parent: Center):
        self.parent = parent

        # 左侧_列表
        self.left_list = QtWidgets.QTableWidget(self.parent.tab_playlist)
        self.left_list.setGeometry(0, 0, 100, 650)
        self.left_list.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.left_list.horizontalHeader().setVisible(False)  # 隐藏水平表头
        self.left_list.verticalScrollBar().setHidden(True)  # 隐藏垂直滚动条
        self.left_list.horizontalScrollBar().setHidden(True)  # 隐藏水平滚动条
        self.left_list.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )  # 设置整行选中

        self.left_list.setColumnCount(1)
        self.left_list.setRowCount(3)

        self.left_list.setItem(0, 0, QtWidgets.QTableWidgetItem("我的列表"))
        self.left_list.setItem(1, 0, QtWidgets.QTableWidgetItem("播放列表"))
        self.left_list.setItem(2, 0, QtWidgets.QTableWidgetItem("我的收藏"))

        self.left_list.item(0, 0).setFont(QtGui.QFont("微软雅黑", 12))

        # 蛇者单元格不可选中
        self.left_list.item(0, 0).setFlags(QtCore.Qt.ItemIsSelectable)

        # 右侧_列表
        self.right_list = QtWidgets.QTableWidget(self.parent.tab_playlist)
        self.right_list.setGeometry(102, 0, 1020, 650)
        self.right_list.setColumnCount(5)
        self.right_list.setHorizontalHeaderLabels(["歌曲名", "歌手", "专辑", "时长", "操作"])

        self.right_list.setColumnWidth(0, 250)
        self.right_list.setColumnWidth(1, 180)
        self.right_list.setColumnWidth(2, 220)
        self.right_list.setColumnWidth(3, 120)
        self.right_list.setColumnWidth(4, 100)

        self.right_list.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )  # 设置整行选中
        self.right_list.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )  # 设置不可编辑
        self.right_list.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed
        )  # 固定单元格尺寸
        self.right_list.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed
        )

        self.event()
        self.style()

    def event(self):
        pass

    def style(self):
        self.left_list.setStyleSheet(
            """
            QTableWidget{
                border:0;
            }

            """
        )


class setting_base:
    def __init__(self, parent: Center):
        self.parent = parent

        # ==== 基本设置

        # 1. 开机自启动
        self.check_startSelf = QtWidgets.QCheckBox(self.parent.tab_setting)
        self.check_startSelf.setText("开机自启动")
        self.check_startSelf.setGeometry(0, 0, 80, 24)

        # 2。 靠边隐藏
        self.check_hideSelf = QtWidgets.QCheckBox(self.parent.tab_setting)
        self.check_hideSelf.setText("靠边隐藏")
        self.check_hideSelf.setGeometry(0, 30, 80, 24)

        # 1. 主题设置

        self.theme_style = 1

        # 2。 动画设置

        self.animation = 1

        # === 播放设置

        # === 搜索设置

        self.event()
        self.style()

    def event(self):
        pass

    def style(self):
        pass
