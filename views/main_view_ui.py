# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_view.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtWidgets import *

from date_time_edit.custom_date_time_edit import DateTimeEdit
from date_time_edit.settings import Mode


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        # MainWindow.resize(250, 86)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.vboxLayout = QVBoxLayout(self.centralwidget)
        self.vboxLayout.setObjectName(u"vboxLayout")

        self.label_even_odd = QLabel(self.centralwidget)
        self.label_even_odd.setObjectName(u"label_even_odd")

        self.vboxLayout.addWidget(self.label_even_odd)

        self.pushButton_reset = QPushButton(self.centralwidget)
        self.pushButton_reset.setObjectName(u"pushButton_reset")
        self.pushButton_reset.setText("Clear")

        self.vboxLayout.addWidget(self.pushButton_reset)

        self.date_time_edit_ps = QDateTimeEdit(self.centralwidget)
        self.date_time_edit_ps.setCalendarPopup(True)
        self.date_time_edit_ps.setObjectName(u"date_time_edit_ps")
        self.date_time_edit_ps.calendarWidget().setLocale(QLocale.English)
        self.date_time_edit_ps.setDisplayFormat("ddd MMM d yyyy HH:mm:ss")
        # self.date_time_edit_ps.calendarWidget().setLocale(
        #     QLocale(QLocale.German, QLocale.Germany)
        # )
        self.vboxLayout.addWidget(self.date_time_edit_ps)

        self.date_time_edit = DateTimeEdit(self.centralwidget, Mode.datetime)
        self.date_time_edit.setObjectName(u"date_time_edit")
        self.date_time_edit.calendarWidget().setLocale(QLocale.English)
        self.vboxLayout.addWidget(self.date_time_edit)

        self.date_edit = DateTimeEdit(self.centralwidget, Mode.date)
        self.date_edit.setObjectName(u"date_edit")
        self.vboxLayout.addWidget(self.date_edit)

        self.time_edit = DateTimeEdit(self.centralwidget, Mode.time)
        self.time_edit.setObjectName(u"time_edit")
        self.time_edit.setDisplayFormat("'Std:'hh 'Min:'mm Sec:ss")
        self.vboxLayout.addWidget(self.time_edit)

        self.date_time_edit_wp = DateTimeEdit(self.centralwidget)
        self.date_time_edit_wp.setCalendarPopup(False)
        self.date_time_edit_wp.setObjectName(u"date_time_edit_wp")
        self.vboxLayout.addWidget(self.date_time_edit_wp)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        pass
    # retranslateUi

