"""
Create-Date: 2021/11/11
Author:Cunfu Peng
Last-Edit-Date: 2021/11
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import qtawesome
from core.play import Player
from core import set

# from gui.ui_main import mainwin
class varname:
    is_play = False
    # 播放模式：["顺序播放","随机播放","循环播放"]
    play_mode = 1
    # 播放音量
    play_voice = 50


class Bottom:
    def __init__(self, parent):
        self.parent = parent
        self.player = Player(self.parent)

        self.frame()
        self.event()
        self.style()

    def frame(self):
        self.bottom = QtWidgets.QLabel(self.parent)
        self.bottom.setGeometry(100, 718, 1144, 70)

        # 歌曲播放信息区域
        self.info = QtWidgets.QLabel(self.bottom)
        self.info.setGeometry(0, 0, 1130, 70)

        # 歌曲播放控制区域
        self.ctrl = QtWidgets.QLabel(self.bottom)
        self.ctrl.setGeometry(870, 2, 150, 24)

        # 歌曲播放播放区域
        self.play = QtWidgets.QLabel(self.bottom)
        self.play.setGeometry(1005, 10, 132, 50)

        # 专辑（小）图片
        self.info_pic = QtWidgets.QLabel(self.info)
        self.info_pic.setGeometry(7, 7, 58, 58)

        # 歌曲 标题
        self.info_title = QtWidgets.QLabel(self.info)
        self.info_title.setGeometry(78, 7, 500, 24)
        self.info_title.setText("年轮 - 张碧晨")

        # 歌曲 播放进度
        self.info_progress = QtWidgets.QSlider(self.info)
        self.info_progress.setGeometry(78, 36, 890, 10)
        self.info_progress.setOrientation(QtCore.Qt.Horizontal)  # 设置为水平滑块条

        # 歌曲 歌词
        self.info_lrc = QtWidgets.QLabel(self.info)
        self.info_lrc.setGeometry(170, 48, 180, 16)
        self.info_lrc.setText("是有缘却无分")

        # 歌曲 当前播放时间
        self.info_time_1 = QtWidgets.QLabel("00:00", self.info)
        self.info_time_1.setGeometry(78, 48, 60, 16)
        self.info_time_1.setText("02:21")

        # 歌曲 总时间
        self.info_time_2 = QtWidgets.QLabel("03:54", self.info)
        self.info_time_2.setGeometry(920, 48, 60, 16)
        self.info_time_2.setText("03:45")

        # style_icon = qtawesome.icon('fa5s.arrow-right',color=123555) # 顺序
        # style_icon = qtawesome.icon('fa5s.sync-alt',color=123555) # 循环
        # style_icon = qtawesome.icon('fa5s.random',color=123555) # 随机
        # self.ctrl_playmode.setIcon(style_icon)
        # style_icon = qtawesome.icon('fa5s.volume-mute',color=123555) # 静音

        # 控制 播放模式
        self.ctrl_playmode = QtWidgets.QPushButton(self.ctrl)
        self.ctrl_playmode.setGeometry(0, 0, 24, 24)
        style_icon = qtawesome.icon("fa5s.arrow-right", color="black")  # 顺序
        self.ctrl_playmode.setIcon(style_icon)

        # 控制 添加到
        self.ctrl_addto = QtWidgets.QPushButton(self.ctrl)
        self.ctrl_addto.setGeometry(28, 0, 24, 24)
        style_icon = qtawesome.icon("fa5s.plus", color="black")  # 添加到
        self.ctrl_addto.setIcon(style_icon)

        # 控制 声音
        self.ctrl_voice = QtWidgets.QPushButton(self.ctrl)
        self.ctrl_voice.setGeometry(54, 0, 24, 24)
        style_icon = qtawesome.icon("fa5s.volume-down", color="black")  # 有声音
        self.ctrl_voice.setIcon(style_icon)

        # 歌曲列表
        self.ctrl_playlist = QtWidgets.QPushButton(self.ctrl)
        self.ctrl_playlist.setGeometry(80, 0, 24, 24)
        style_icon = qtawesome.icon("fa5s.bars", color="black")  # 列表
        self.ctrl_playlist.setIcon(style_icon)

        # 控制 上一首
        self.play_up = QtWidgets.QPushButton(self.play)
        self.play_up.setGeometry(0, 16, 32, 32)
        style_icon = qtawesome.icon("fa5s.angle-double-left", color="black")  # 上一首
        self.play_up.setIcon(style_icon)

        # 控制 播放
        self.play_pause = QtWidgets.QPushButton(self.play)
        self.play_pause.setGeometry(40, 0, 48, 48)
        style_icon = qtawesome.icon("fa5s.play", color="black")  # 播放
        self.play_pause.setIcon(style_icon)

        # 控制 下一首
        self.play_down = QtWidgets.QPushButton(self.play)
        self.play_down.setGeometry(96, 16, 32, 32)
        style_icon = qtawesome.icon("fa5s.angle-double-right", color="black")  # 下一首
        self.play_down.setIcon(style_icon)

    def event(self):
        self.ctrl_playlist.clicked.connect(self.playList)
        self.ctrl_addto.clicked.connect(self.addTo)
        self.ctrl_voice.clicked.connect(self.ctrlVoice)
        self.ctrl_playmode.clicked.connect(self.playMode)
        self.play_up.clicked.connect(self.playUp)
        self.play_pause.clicked.connect(self.playPause)
        self.play_down.clicked.connect(self.playDown)
        # self.info_pic.mousePressEvent(QtGui.QMouseEvent())

        self.info_progress.valueChanged.connect(self.sliderValueChanged)

        """
        1、 QProgressBar基本用法
        m_pConnectProBar = new QProgressBar;
        m_pConnectProBar->setRange(0,100); //设置进度条最小值和最大值(取值范围)
        m_pConnectProBar->setMinimum(0); //设置进度条最小值
        m_pConnectProBar->setMaximum(100); //设置进度条最大值
        m_pConnectProBar->setValue(50);  //设置当前的运行值
        m_pConnectProBar->reset(); //让进度条重新回到开始
        m_pConnectProBar->setOrientation(Qt::Horizontal);  //水平方向
        m_pConnectProBar->setOrientation(Qt::Vertical);  //垂直方向
        m_pConnectProBar->setAlignment(Qt::AlignVCenter);  // 对齐方式 
        m_pConnectProBar->setTextVisible(false); //隐藏进度条文本
        m_pConnectProBar->setFixedSize(258,5);   //进度条固定大小
        m_pConnectProBar->setInvertedAppearance(true); //true:反方向  false:正方向
        m_pConnectProBar->setVisible(false);  //false:隐藏进度条  true:显示进度条
        """
        """
        [2]信号
        QSlider常用的信号有以下这几个信号:
        
        移动滑动条时发出的信号:
        
        void sliderMoved(int value)
        其传递的参数为当前滑动条所对应的数值
        
        点击滑动条时所发出的信号:
        void sliderPressed()
        
        释放时所发出的信号:
        void sliderReleased()
        
        数值改变时所发出的信号：
        void valueChanged(int value)
        """

    def info_pic_mouse_down(self):
        if set.IS_DEBUG:
            print("info-pic 接收 鼠标按钮下 消息")

    def sliderValueChanged(self):
        if set.IS_DEBUG:
            print("滑动条的值改变")

    def playList(self):
        if set.IS_DEBUG:
            print("播放列表")

    def addTo(self):
        if set.IS_DEBUG:
            print("添加到")

    def ctrlVoice(self):
        if set.IS_DEBUG:
            print("调节音量")
        # SELF CODE
        if varname.play_voice == 0:
            if set.IS_DEBUG:
                print("静音")
            # CODE
            style_icon = qtawesome.icon("fa5s.volume-off", color="black")  # 有声音
            self.ctrl_voice.setIcon(style_icon)

        else:
            if set.IS_DEBUG:
                print("非静音")
            # CODE
            style_icon = qtawesome.icon("fa5s.volume", color="black")  # 有声音
            self.ctrl_voice.setIcon(style_icon)

    def playMode(self):
        if set.IS_DEBUG:
            print("播放模式")

        if self.player.getPlayMode() == 1:
            if set.IS_DEBUG:
                print("顺序播放")
            # SELF CODE
            self.player.setPlayMode(2)
            # 设置图标
            style_icon = qtawesome.icon("fa5s.axe", color="black")  # 播放
            self.ctrl_playmode.setIcon(style_icon)
            return
        if self.player.getPlayMode() == 2:
            if set.IS_DEBUG:
                print("随机播放")
            # SELF CODE
            self.player.setPlayMode(3)
            # 设置图标
            style_icon = qtawesome.icon("fa5s.atom-alt", color="black")  # 播放
            self.ctrl_playmode.setIcon(style_icon)
            return
        if self.player.getPlayMode() == 3:
            if set.IS_DEBUG:
                print("循环播放")
            # SELF CODE
            self.player.setPlayMode(1)
            # 设置图标
            style_icon = qtawesome.icon("fa5s.pause", color="black")  # 播放
            self.ctrl_playmode.setIcon(style_icon)
            return

    def playUp(self):
        if set.IS_DEBUG:
            print("上一首")
        self.player.previous()

    def playPause(self):
        if set.IS_DEBUG:
            print("播放暂停")
        # SELF CODE

        if self.player.isPlayNow():
            if set.IS_DEBUG:
                print("暂停")
            # SELF CODE
            self.player.pause()
            # 设置播放图标
            style_icon = qtawesome.icon("fa5s.play", color="black")  # 播放
            self.play_pause.setIcon(style_icon)
        else:
            if set.IS_DEBUG:
                print("播放")
            # SELF CODE
            self.player.play()
            # 设置暂停图标
            style_icon = qtawesome.icon("fa5s.pause", color="black")  # 播放
            self.play_pause.setIcon(style_icon)

    def playDown(self):
        if set.IS_DEBUG:
            print("下一首")
        self.player.next()

    def style(self):
        # self.bottom.setStyleSheet("background-color:red;")
        self.info_pic.setStyleSheet(
            """
        QLabel { 
            background-color:green;
        }
        """
        )

        self.info_title.setStyleSheet(
            """
        QLabel {
            font-family:"微软雅黑";
        }
        """
        )

        self.info_lrc.setStyleSheet(
            """
        QLabel {
            font-family:"微软雅黑";
            
        }
        """
        )

        self.info_time_1.setStyleSheet(
            """
        QLabel {
            font-family:"微软雅黑";
        }
        """
        )
        self.info_time_2.setStyleSheet(
            """
        QLabel {
            font-family:"微软雅黑";
        }
        """
        )

        self.ctrl_playmode.setStyleSheet(
            """
        QPushButton { 
            border:none;
            border-radius:15px;
            background-color:rgb(209,232,247);
        } 
        QPushButton:hover { 
            background-color:rgb(129,191,233);
        }
        """
        )

        self.ctrl_addto.setStyleSheet(
            """
        QPushButton {
            background-color:rgb(209,232,247);
            border:none;
            border-radius:15px;
        } 
        QPushButton:hover {
            background-color:rgb(129,191,233);
        }
        """
        )

        self.ctrl_voice.setStyleSheet(
            """
        QPushButton {
            background-color:rgb(209,232,247);
            border:none;
            border-radius:15px;
        } 
        QPushButton:hover {
            background-color:rgb(129,191,233);
        }"""
        )

        self.ctrl_playlist.setStyleSheet(
            """
        QPushButton {
            background-color:rgb(209,232,247);
            border:none;
            border-radius:15px;
        } 
        QPushButton:hover {
            background-color:rgb(129,191,233);
        }
        """
        )
        self.play_up.setStyleSheet(
            """
        QPushButton{
            border:none;
            border-radius:15px;
            background-color:rgb(209,232,247);
        }
        QPushButton:hover{
            background-color:rgb(129,191,233);
        }
        """
        )

        self.play_pause.setStyleSheet(
            """
        QPushButton{
            border:none;
            border-radius:22px;
            background-color:rgb(209,232,247);
        }
        QPushButton:hover{
            background-color:rgb(129,191,233);
        }
        """
        )

        self.play_down.setStyleSheet(
            """
        QPushButton{
            background-color:rgb(209,232,247);
            border:none;
            border-radius:15px;
        }
        QPushButton:hover{
            background-color:rgb(129,191,233);
        }
        """
        )


class methods(Bottom):
    def __init__(self):
        pass


class list_base:
    def __init__(self, parent: Bottom):
        self.parent = parent

        self.a = QtWidgets.QTableWidget(self.parent.parent)
        # self.a.setGeometry(800, 250, 300, 460)
        self.a.setGeometry(800, 210, 300, 500)
        self.a.setColumnCount(2)
        self.a.setColumnWidth(0, 130)
        self.a.setColumnWidth(1, 120)
        self.a.setHorizontalHeaderLabels(["歌曲名", "歌手"])
        self.a.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.a.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # 设置整行选中
        self.a.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed
        )  # 使用户无法调整
        self.a.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

        self.event()
        self.style()

    def event(self):
        self.a.clicked.connect(self.playMusic)

    def setShow(self):
        if self.a.isVisible():
            print("not show")
            self.a.setVisible(False)
        else:
            print("show")
            self.a.setVisible(True)

    def playMusic(self):
        playlist = Player.playlist(self.parent.path.songDB + "\\songlist.db")
        playlist.index = self.a.currentRow() + 1

        song_id = playlist.getLocalMusicInfo()[1]
        song_id = "1456890009"
        music_path = "http://music.163.com/song/media/outer/url?id={0}.mp3".format(
            song_id
        )
        print(music_path)
        Player.music(self.parent).play(music_path, "url")

    def style(self):
        pass


class Picture(QtWidgets.QLabel):
    mylabelSig = QtCore.pyqtSignal(str)
    mylabelDoubleClickSig = QtCore.pyqtSignal(str)

    def __int__(self):
        super(Picture, self).__init__()

    def mouseDoubleClickEvent(self, e):  # 双击
        sigContent = self.objectName()
        self.mylabelDoubleClickSig.emit(sigContent)

    def mousePressEvent(self, e):  # 单击
        sigContent = self.objectName()
        self.mylabelSig.emit(sigContent)

    def leaveEvent(self, e):  # 鼠标离开label
        print("leaveEvent")

    def enterEvent(self, e):  # 鼠标移入label
        print("enterEvent")
