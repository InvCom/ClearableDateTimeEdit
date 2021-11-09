# -*- coding: utf-8 -*-
import sys

from PySide2.QtWidgets import QApplication, QMainWindow

from views.main_view import MainView


class MainApplication(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainApplication, self).__init__(*args, **kwargs)
        self.main_view = MainView()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApplication()
    window.main_view.show()
    sys.exit(app.exec_())
