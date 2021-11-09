# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'datetime1.ui',
# licensing of 'datetime1.ui' applies.
#
# Created: Mon Oct 11 17:58:33 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import Qt

from ClearableDateTimeEdit.popup.TimeWidget import TimeWidget


class DateTimePopupUi(object):
    def __init__(self):
        super(DateTimePopupUi, self).__init__()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowFlags(Qt.Popup)
        Form.resize(510, 235)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        # Form.setMinimumSize(QtCore.QSize(510, 235))
        Form.setMaximumSize(QtCore.QSize(500, 235))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setContentsMargins(4, 2, 4, 2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.calendarWidget = QtWidgets.QCalendarWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendarWidget.sizePolicy().hasHeightForWidth())
        self.calendarWidget.setSizePolicy(sizePolicy)
        self.calendarWidget.setMaximumSize(QtCore.QSize(312, 16777215))
        self.calendarWidget.setStyleSheet("margin: 0px;")
        self.calendarWidget.setObjectName("calendarWidget")
        self.horizontalLayout_2.addWidget(self.calendarWidget)
        self.timeWidget = TimeWidget(Form)
        self.horizontalLayout_2.addWidget(self.timeWidget)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.nowButton = QtWidgets.QPushButton(Form)
        self.nowButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.nowButton)
        self.clearButton = QtWidgets.QPushButton(Form)
        self.clearButton.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.clearButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.submitButton = QtWidgets.QPushButton(Form)
        self.submitButton.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.submitButton)
        self.cancelButton = QtWidgets.QPushButton(Form)
        self.cancelButton.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.nowButton.setText(QtWidgets.QApplication.translate("Form", "Now", None, -1))
        self.clearButton.setText(QtWidgets.QApplication.translate("Form", "Clear", None, -1))
        self.submitButton.setText(QtWidgets.QApplication.translate("Form", "Ok", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("Form", "Cancel", None, -1))
