# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'time_widget.ui',
# licensing of 'time_widget.ui' applies.
#
# Created: Mon Nov  8 17:03:15 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 268)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(300, 300))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.timeWidgetVerticalLayout = QtWidgets.QVBoxLayout()
        self.timeWidgetVerticalLayout.setObjectName("timeWidgetVerticalLayout")
        self.timeLabel = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeLabel.sizePolicy().hasHeightForWidth())
        self.timeLabel.setSizePolicy(sizePolicy)
        self.timeLabel.setMinimumSize(QtCore.QSize(0, 22))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.timeLabel.setFont(font)
        self.timeLabel.setStyleSheet("background-color: rgb(85, 0, 255);\n"
"color: rgb(255, 255, 255);\n"
"margin: 0px;")
        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.timeWidgetVerticalLayout.addWidget(self.timeLabel)
        self.timeWidgetHorizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.timeWidgetHorizontalLayout_3.setSpacing(0)
        self.timeWidgetHorizontalLayout_3.setObjectName("timeWidgetHorizontalLayout_3")

        self.hourVerticalLayout = QtWidgets.QVBoxLayout()
        self.hourVerticalLayout.setSpacing(0)
        self.hourVerticalLayout.setObjectName("hourVerticalLayout")
        self.hourLabel = QtWidgets.QLabel(Form)
        self.hourLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.hourLabel.setObjectName("hourLabel")
        self.hourVerticalLayout.addWidget(self.hourLabel)
        self.hourListView = QtWidgets.QListView(Form)
        self.hourListView.setMaximumSize(QtCore.QSize(40, 16777215))
        self.hourListView.setStyleSheet("margin: 0px;")
        self.hourListView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.hourListView.setObjectName("hourListView")
        self.hourVerticalLayout.addWidget(self.hourListView)
        self.timeWidgetHorizontalLayout_3.addLayout(self.hourVerticalLayout)
        self.minVerticalLayout = QtWidgets.QVBoxLayout()
        self.minVerticalLayout.setSpacing(0)
        self.minVerticalLayout.setObjectName("minVerticalLayout")
        self.minLabel = QtWidgets.QLabel(Form)
        self.minLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.minLabel.setObjectName("minLabel")
        self.minVerticalLayout.addWidget(self.minLabel)
        self.minListView = QtWidgets.QListView(Form)
        self.minListView.setMaximumSize(QtCore.QSize(40, 16777215))
        self.minListView.setObjectName("minListView")
        self.minVerticalLayout.addWidget(self.minListView)
        self.timeWidgetHorizontalLayout_3.addLayout(self.minVerticalLayout)
        self.secVerticalLayout = QtWidgets.QVBoxLayout()
        self.secVerticalLayout.setSpacing(0)
        self.secVerticalLayout.setObjectName("secVerticalLayout")
        self.secLabel = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.secLabel.sizePolicy().hasHeightForWidth())
        self.secLabel.setSizePolicy(sizePolicy)
        self.secLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.secLabel.setObjectName("secLabel")
        self.secVerticalLayout.addWidget(self.secLabel)
        self.secListView = QtWidgets.QListView(Form)
        self.secListView.setMaximumSize(QtCore.QSize(40, 16777215))
        self.secListView.setObjectName("secListView")
        self.secVerticalLayout.addWidget(self.secListView)
        self.timeWidgetHorizontalLayout_3.addLayout(self.secVerticalLayout)
        self.timeWidgetVerticalLayout.addLayout(self.timeWidgetHorizontalLayout_3)
        self.msecLineEdit = QtWidgets.QLineEdit(Form)
        self.msecLineEdit.setText("")
        self.msecLineEdit.setObjectName("msecLineEdit")
        self.timeWidgetVerticalLayout.addWidget(self.msecLineEdit)
        self.verticalLayout.addLayout(self.timeWidgetVerticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "TimeWidget", None, -1))
        self.timeLabel.setText(QtWidgets.QApplication.translate("Form", "Time", None, -1))
        self.hourLabel.setText(QtWidgets.QApplication.translate("Form", "h", None, -1))
        self.minLabel.setText(QtWidgets.QApplication.translate("Form", "m", None, -1))
        self.secLabel.setText(QtWidgets.QApplication.translate("Form", "s", None, -1))

