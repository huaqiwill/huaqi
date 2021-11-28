"""
@ File-Name：play.py
@ Author: Cunfu Peng
@ Create-Date：2021/11/24
@ Last-Update-Date：2021/11/24
"""

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import random
import time


class Player:
    def __init__(self, parent):
        self._playList = []
        self._currentIndex = 0
        self._progress = 0
        self._speed = 1  # 速度的值控制在 0.5~1.5 之间，超出不生效
        self._playMode = 1  # 三个模式，值只能为 1,2,3
        self._volume = 50

        self.__minCount = 0
        self.__maxCount = 0

        self.__isPause = False

        self.__media = QMediaPlayer(parent)

    def play(self):  # 播放
        """
        播放
        """
        if self.__isPause:
            self.__media.play()
            self.__isPause = False
        else:
            self.__isPause = True
            self.__media.stop()
            play = self._playList[self._currentIndex]
            if play["sourcefrom"] == "native":
                url = QUrl.fromLocalFile(play["path"])
            if play["sourcefrom"] == "url":
                url = QUrl(play["path"])

            self.__media.setMedia(QMediaContent(url))
            self.__media.setVolume(self._volume)
            self.__media.play()

    def pause(self) -> None:  # 暂停
        """
        暂停
        """
        self.__media.pause()
        self.__isPause = True

    def stop(self) -> None:
        """
        停止
        """
        self.__media.stop()
    
    def isPlayNow(self) -> bool:
        return bool(~self.__isPause)

    def next(self) -> None:  # 下一首
        """
        下一首，受播放模式影响
        """
        if self._playMode == 1 or self._playMode == 3:  # 顺序播放和循环播放
            if self._currentIndex != self.__maxCount:
                self._currentIndex += 1

        if self._playMode == 2:  # 随机播放
            self._currentIndex = random.randint(self.__minCount-1, self.__maxCount+1)

    def previous(self) -> None:  # 上一首
        """
        上一首，受播放模式影响
        """
        if self._playMode == 1 or self._playMode == 3:  # 顺序播放和循环播放
            if self._currentIndex != self.__minCount:
                self._currentIndex -= 1

        if self._playMode == 2:  # 随机播放
            self._currentIndex = random.randint(self.__minCount-1, self.__maxCount+1)


    def setProgress(self, progress):
        """
        设置播放进度
        """
        self._progress = progress

    def getProgress(self):
        """
        获取播放进度
        """
        return self._progress

    def setSpeed(self, speed):
        """
        设置播放速度
        """
        self._speed = speed

    def getSpeed(self):
        """
        获取播放速度
        """
        return self._speed

    def setCurrentIndex(self, currentIndex) -> None:
        """
        设置当前播放索引
        """
        self._currentIndex = currentIndex

    def getCurrentIndex(self) -> int:
        """
        获取当前播放索引
        """
        return self._currentIndex

    def setPlayMode(self, playMode: int):
        """
        设置播放模式
        1. 顺序播放
        2. 随机播放
        3. 循环播放
        """
        self._playMode = playMode

    def getPlayMode(self) -> int:
        """
        获取播放模式
        1. 顺序播放
        2. 随机播放
        3. 循环播放
        """
        return self._playMode

    def setVolume(self, volume: int) -> None:
        """
        设置音量
        """
        self._volume = volume

    def getVolume(self) -> int:
        """
        获取音量
        """
        return self._volume

    def setPlaylist(self, list:list):
        self._playList = list
        self.__maxCount = self._playList.__len__()

    def getPlaylist(self) -> list:
        return self._playList

    def addIn(self, path) -> None:  # 增
        """
        增
        1. object path：传入一个对象，例如{"sourcefrom":"native","path":"C:\\test.mp3"}，{"sourcefrom":"url","path":"http://test.com/test.mp3"}
            sourcefrom：可供选择的有两个值（"native"和"url"）
        """
        self._playList.append(path)
        self.__maxCount = self._playList.__len__()

    def deleteIn(self, index: int) -> None:  # 删
        """
        删
        1. int index：索引
        """
        self._playList.pop(index)
        self.__maxCount = self._playList.__len__()

    def getIn(self, index: int = -1):  # 查
        """
        查
        1. int index：默认为-1，返回全部。
            不为1则返回索引所在的值

        返回值：默认返回列表，否则返回对象{"sourcefrom":" ","path":" "}
        """
        if index == -1:
            return self._playList
        return self._playList[index]

    def insertIn(self, index, path: object) -> None:  # 插
        """
        插
        1. int index：插入索引
        2. object path：传入一个对象，例如{"sourcefrom":"native","path":"C:\\test.mp3"}，{"sourcefrom":"url","path":"http://test.com/test.mp3"}
            sourcefrom：可供选择的有两个值（"native"和"url"）
        """
        self._playList.insert(index, path)
        self.__maxCount = self._playList.__len__()

    def updateIn(self, index: int, path: object) -> None:  # 改
        """
        改
        1. int index：更新索引
        2.  object path：传入一个对象，例如{"sourcefrom":"native","path":"C:\\test.mp3"}，{"sourcefrom":"url","path":"http://test.com/test.mp3"}
            sourcefrom：可供选择的有两个值（"native"和"url"）
        """
        self._playList[index] = path



# from PyQt5.QtWidgets import QApplication,QMainWindow
# app = QApplication([])
# win = QMainWindow()
# win.show()
# app.exec()
