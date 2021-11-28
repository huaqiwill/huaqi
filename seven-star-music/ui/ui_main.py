# package gui.ui_main
"""
@ File-Name: ui_main.py
@ Author: Cunfu Peng
@ Date: 2021/09/18
@ Last-Edit-Date: 2021/11
@ Version: 2.0
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from core import set

"""
上 -> 下    参数
下 -> 上    返回
"""

from ui import ui_bottom, ui_center, ui_nav, ui_top


class MainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        if set.IS_DEBUG:
            print("程序正在启动中...")

        self.frame()
        set.loadSet()

    def frame(self):
        # 设置任务栏图标
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        self.setFixedSize(1244, 788)

        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setWindowOpacity(0.99)  # 设置窗口透明度
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        # 设置圆角边框
        self.bmp = QtGui.QBitmap(1244, 788)  # 这里将window size引入，否则无效果！
        self.bmp.fill()
        self.Painter = QtGui.QPainter(self.bmp)
        self.Painter.setPen(QtCore.Qt.NoPen)
        self.Painter.setBrush(QtCore.Qt.black)
        self.Painter.drawRoundedRect(self.bmp.rect(), 10, 10)  # 倒边角为5px
        self.setMask(self.bmp)  # 切记将self.bmp Mark到window

        self.nav = ui_nav.Nav(self)
        self.top = ui_top.Top(self)
        self.bottom = ui_bottom.Bottom(self)
        self.center = ui_center.Center(self)

    # ===================== # ===================== #
    # 无边框的拖动 事件重写
    # ===
    def mouseMoveEvent(self, e: QtGui.QMouseEvent):  # 重写移动事件
        if self._isTracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            self._isTracking = True
            self._startPos = QtCore.QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    # ===================== # ===================== #
