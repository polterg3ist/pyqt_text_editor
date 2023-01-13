from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QFileDialog, QMessageBox, QPushButton, QHBoxLayout, QShortcut

import sys


class Window(QMainWindow):
    def __init__(self, app):
        super(Window, self).__init__()

        self.screen = app.primaryScreen()
        self.size = self.screen.size()

        self.window_title = "Text Editor"

        self.setWindowIcon(QtGui.QIcon('my_icon_0.png'))

        self.screen_width = self.size.width()
        self.screen_height = self.size.height()

        self.window_width = 800
        self.window_height = 600

        self.window_start_pos_x = self.screen_width // 2 - self.window_width // 2
        self.window_start_pos_y = self.screen_height // 2 - self.window_height // 2

        self.setWindowTitle(self.window_title)
        self.setGeometry(self.window_start_pos_x, self.window_start_pos_y, self.window_width, self.window_height)

        self.text_edit = QtWidgets.QTextEdit(self)

        self.setCentralWidget(self.text_edit)

        self.create_menu_bar()

        self.save_shortcut = QShortcut(QKeySequence("Ctrl+s"), self)
        self.open_shortcut = QShortcut(QKeySequence("Ctrl+o"), self)
        self.zoom_in_shortcut = QShortcut(QKeySequence("Ctrl+="), self)
        self.zoom_out_shortcut = QShortcut(QKeySequence("Ctrl+-"), self)

        self.save_shortcut.activated.connect(self.action_save)
        self.open_shortcut.activated.connect(self.action_open)
        self.zoom_in_shortcut.activated.connect(self.action_zoom_in)
        self.zoom_out_shortcut.activated.connect(self.action_zoom_out)

    def create_menu_bar(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        file_menu = QMenu("&Menu", self)
        menu_bar.addMenu(file_menu)

        open_file = file_menu.addAction("Open", self.action_clicked)
        save_file = file_menu.addAction("Save", self.action_clicked)

    @QtCore.pyqtSlot()
    def action_clicked(self):
        action = self.sender()
        action_text = action.text()

        if action_text == "Open":
            self.action_open()
        elif action_text == "Save":
            self.action_save()

    def error_btn_click(self, btn):
        btn_text = btn.text()
        if btn_text == "Open":
            self.action_open()
        elif btn_text == "Cancel":
            self.text_edit.setText("")

    def error_window(self, error):
        error_window = QMessageBox()
        error_window.setWindowTitle("Error")
        error_window.setText("ERROR")
        error_window.setIcon(QMessageBox.Warning)
        error_window.setStandardButtons(QMessageBox.Cancel | QMessageBox.Open)
        error_window.setDefaultButton(QMessageBox.Open)
        error_window.setInformativeText("An error occurred while opening/saving file")
        error_window.setDetailedText(f"{error}")
        error_window.exec_()

    @QtCore.pyqtSlot()
    def action_open(self):
        opened_file = QFileDialog.getOpenFileName(self)[0]
        try:
            with open(opened_file, "r") as file:
                data = file.read()
                self.text_edit.setText(data)
        except Exception as error:
            self.error_window(error)

    @QtCore.pyqtSlot()
    def action_save(self):
        try:
            opened_file = QFileDialog.getSaveFileName(self)[0]
            with open(opened_file, "w") as file:
                text = self.text_edit.toPlainText()
                file.write(text)
        except Exception as error:
            self.error_window(error)

    @QtCore.pyqtSlot()
    def action_zoom_in(self):
        self.text_edit.zoomIn(2)

    @QtCore.pyqtSlot()
    def action_zoom_out(self):
        self.text_edit.zoomOut(2)


def application():
    app = QApplication(sys.argv)
    window = Window(app)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
