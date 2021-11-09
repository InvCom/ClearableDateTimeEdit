import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *


class EditDate:

    def __init__(self):
        super(EditDate, self).__init__()
        self.app_runner()

    def date_gui(self):
        self.app = QApplication(sys.argv)
        self.win = QDialog()
        self.win.setFixedSize(280, 40)


        self.dateEdit = QDateEdit(self.win)
        self.dateEdit.setFixedSize(230, 40)
        self.dateEdit.move(5, 0)

        self.hideCalendar = QPushButton(self.win)
        self.hideCalendar.setText("Hide")
        self.hideCalendar.move(231, 0)
        self.hideCalendar.setFixedSize(45, 40)

        self.displayCalendar = QPushButton(self.win)
        self.displayCalendar.setText("Date..")
        self.displayCalendar.move(231, 0)
        self.displayCalendar.setFixedSize(45, 40)

        self.calender = QCalendarWidget(self.win)
        self.calender.move(5, 40)

        self.todayButton = QPushButton(self.win)
        self.todayButton.setText("Today")
        self.todayButton.setFixedSize(100, 30)
        self.todayButton.move(5, 200)

        self.calender.hide()
        self.todayButton.hide()

    def button_handling(self):
        self.todayButton.clicked.connect(self.todays_date)
        self.displayCalendar.clicked.connect(self.display_cal)
        self.hideCalendar.clicked.connect(self.hide_cal)

    def hide_cal(self):
        self.calender.hide()
        self.displayCalendar.show()
        self.todayButton.hide()
        self.hideCalendar.hide()
        self.win.setFixedSize(280, 40)

    def display_cal(self):
        self.win.setFixedSize(280, 300)
        self.calender.show()
        self.todayButton.show()
        self.hideCalendar.show()
        self.displayCalendar.hide()

    def todays_date(self):
        self.date = QDate.currentDate()
        self.dateEdit.setDate(self.date)
        self.calender.setSelectedDate(self.date)

    def app_runner(self):
        self.date_gui()
        self.win.show()
        self.button_handling()
        sys.exit(self.app.exec_())

main = EditDate()