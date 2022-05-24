# -*- coding: utf-8 -*-
__all__ = ["TimeWidget"]
from PySide2.QtCore import QSize, Qt, QTime
from PySide2.QtGui import QFont, QIntValidator
from PySide2.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QSizePolicy,
    QHBoxLayout,
    QListWidget,
    QLineEdit, QApplication, QListWidgetItem,
)


class TimeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.__maximumTime = QTime(23, 59, 59, 999)
        self.__minimumTime = QTime(0, 0, 0, 0)
        # self._timeSpec = Qt.TimeSpec.LocalTime
        self.setupTime()

    def init_ui(self):
        self.setObjectName("TimeWidget")
        # self.resize(200, 210)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(0, 0))
        self.setMaximumSize(QSize(320, 182))
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.timeLabel = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeLabel.sizePolicy().hasHeightForWidth())
        self.timeLabel.setSizePolicy(sizePolicy)
        self.timeLabel.setMinimumSize(QSize(0, 22))
        font = QFont()
        font.setWeight(75)
        font.setBold(True)
        self.timeLabel.setFont(font)
        self.timeLabel.setStyleSheet(
            "background-color: rgb(0, 122, 212);\n"
            "color: rgb(255, 255, 255);\n"
            "margin: 0px;"
        )
        self.timeLabel.setAlignment(Qt.AlignCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.verticalLayout.addWidget(self.timeLabel)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        labelStylesheet = "border: 1px solid grey;"
        self.hourVerticalLayout = QVBoxLayout()
        self.hourVerticalLayout.setObjectName("hourVerticalLayout")
        self.hourLabel = QLabel()
        self.hourLabel.setAlignment(Qt.AlignCenter)
        self.hourLabel.setStyleSheet(labelStylesheet)
        self.hourLabel.setObjectName("hourLabel")
        self.hourVerticalLayout.addWidget(self.hourLabel)
        self.hourListWidget = QListWidget(self)
        # self.hourListWidget.setMaximumSize(QtCore.QSize(50, 16777215))
        self.hourListWidget.setStyleSheet("margin: 0px;")
        self.hourListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.hourListWidget.setObjectName("hourListWidget")
        self.hourVerticalLayout.addWidget(self.hourListWidget)
        self.horizontalLayout_3.addLayout(self.hourVerticalLayout)
        self.minVerticalLayout = QVBoxLayout()
        self.minVerticalLayout.setObjectName("minVerticalLayout")
        self.minLabel = QLabel(self)
        self.minLabel.setAlignment(Qt.AlignCenter)
        self.minLabel.setStyleSheet(labelStylesheet)
        self.minLabel.setObjectName("minLabel")
        self.minVerticalLayout.addWidget(self.minLabel)
        self.minListWidget = QListWidget(self)
        # self.minListWidget.setMaximumSize(QtCore.QSize(50, 16777215))
        self.minListWidget.setObjectName("minListWidget")
        self.minListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.minVerticalLayout.addWidget(self.minListWidget)
        self.horizontalLayout_3.addLayout(self.minVerticalLayout)
        self.secVerticalLayout = QVBoxLayout()
        self.secVerticalLayout.setObjectName("secVerticalLayout")
        self.secLabel = QLabel(self)
        self.secLabel.setAlignment(Qt.AlignCenter)
        self.secLabel.setStyleSheet(labelStylesheet)
        self.secLabel.setObjectName("secLabel")
        self.secVerticalLayout.addWidget(self.secLabel)
        self.secListWidget = QListWidget(self)
        # self.secListWidget.setMaximumSize(QtCore.QSize(50, 16777215))
        self.secListWidget.setObjectName("secListWidget")
        self.secListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.secVerticalLayout.addWidget(self.secListWidget)
        self.horizontalLayout_3.addLayout(self.secVerticalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.msecHorizontalLayout = QHBoxLayout()
        self.msecHorizontalLayout.setObjectName("msecHorizontalLayout")
        self.msecLabel = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.msecLabel.sizePolicy().hasHeightForWidth())
        self.msecLabel.setSizePolicy(sizePolicy)
        self.msecLabel.setAlignment(Qt.AlignCenter)
        self.msecLabel.setStyleSheet(labelStylesheet)
        self.msecLabel.setMaximumSize(QSize(40, 22))
        self.msecLabel.setMinimumWidth(30)
        self.msecLabel.setObjectName("msecLabel")
        self.msecHorizontalLayout.addWidget(self.msecLabel)
        self.msecLineEdit = QLineEdit(self)
        self.msecLineEdit.setPlaceholderText("msec")
        self.msecLineEdit.setObjectName("msecLineEdit")
        self.msecHorizontalLayout.addWidget(self.msecLineEdit)
        self.verticalLayout.addLayout(self.msecHorizontalLayout)

        self.timeLabel.setText(QApplication.translate("TimeWidget", "Time", None, -1))
        self.hourLabel.setText(QApplication.translate("TimeWidget", "h", None, -1))
        self.minLabel.setText(QApplication.translate("TimeWidget", "m", None, -1))
        self.secLabel.setText(QApplication.translate("TimeWidget", "s", None, -1))
        self.msecLabel.setText(QApplication.translate("TimeWidget", "ms:", None, -1))

    def minimumTime(self):
        return self.__minimumTime

    def setMinimumTime(self, min_time):
        if not isinstance(min_time, QTime):
            min_type = str(type(min_time)).split("'")[1]
            raise TypeError(
                f"""'TimeWidget.setMinimumTime' called with wrong argument types:\n\t
                TimeWidget.setMinimumTime({min_type})\n\t\t
                Supported signatures:\n\t
                TimeWidget.setMinimumTime(PySide2.QtCore.QTime)"""
            )
        self.__minimumTime = min_time
        self.setupTime()

    def clearMinimumTime(self):
        self.__minimumTime = QTime(0, 0, 0, 0)
        self.setupTime()

    def maximumTime(self):
        return self.__maximumTime

    def setMaximumTime(self, max_time):
        if not isinstance(max_time, QTime):
            max_type = str(type(max_time)).split("'")[1]
            raise TypeError(
                f"""'TimeWidget.setMaximumTime' called with wrong argument types:\n\t
                TimeWidget.setMaximumTime({max_type})\n\t\t
                Supported signatures:\n\t
                TimeWidget.setMaximumTime(PySide2.QtCore.QTime)"""
            )
        self.__maximumTime = max_time
        self.setupTime()

    def clearMaximumTime(self):
        self.__maximumTime = QTime(23, 59, 59, 999)
        self.setupTime()

    def setupTime(self):
        hours = [QListWidgetItem(str(i)) for i in range(self.__minimumTime.hour(), self.__maximumTime.hour() + 1)]
        minutes = [QListWidgetItem(str(i)) for i in range(self.__minimumTime.minute(), self.__maximumTime.minute() + 1)]
        seconds = [QListWidgetItem(str(i)) for i in range(self.__minimumTime.second(), self.__maximumTime.second() + 1)]
        for time_widget, time_list in zip(
                [
                    self.hourListWidget,
                    self.minListWidget,
                    self.secListWidget,
                ],
                [hours, minutes, seconds],
        ):
            time_widget.clear()
            for item in time_list:
                time_widget.addItem(item)
            time_widget.setCurrentItem(time_list[0])
        int_val = QIntValidator()
        int_val.setRange(self.__minimumTime.msec(), self.__maximumTime.msec())
        self.msecLineEdit.setValidator(int_val)

    def reset(self):
        self.hourListWidget.setCurrentRow(0)
        self.minListWidget.setCurrentRow(0)
        self.secListWidget.setCurrentRow(0)
        self.msecLineEdit.setText("")

    def setToday(self):
        now = QTime.currentTime()
        self.hourListWidget.setCurrentRow(now.hour())
        self.minListWidget.setCurrentRow(now.minute())
        self.secListWidget.setCurrentRow(now.second())
        self.msecLineEdit.setText(str(now.msec()))

    def showMsec(self, show: bool = True):
        self.msecLineEdit.setVisible(show)
        self.msecLabel.setVisible(show)

    def setTime(self, new_time):
        self.hourListWidget.setCurrentRow(new_time.hour())
        self.minListWidget.setCurrentRow(new_time.minute())
        self.secListWidget.setCurrentRow(new_time.second())
        self.msecLineEdit.setText(str(new_time.msec()))
