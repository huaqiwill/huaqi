"""
@ Project-Name:seven-star-music
@ File-Name: seven-star-music.py 
@ Author: Cunfu Peng
@ Create-Date: 2021/09/18
@ Last-Update: 2021/11/24
@ Version: 2.1
"""
import ui.ui_main as gui

if __name__ == "__main__":
    app = gui.QtWidgets.QApplication([])
    ui = gui.MainWin()
    print("启动成功！")
    ui.show()
    app.exec_()
