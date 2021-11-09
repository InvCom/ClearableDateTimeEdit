# -*- coding: utf-8 -*-
from PySide2.QtCore import QObject, QDate
from PySide2.QtWidgets import QWidget, QCalendarWidget

from ClearableDateTimeEdit.Settings import Mode
from ClearableDateTimeEdit.popup.DateTimePopupUi import DateTimePopupUi
from ClearableDateTimeEdit.popup.Helpers import CustomTimeHelper, CustomDateTimeHelper, CustomDateHelper


class DateTimePopup(QWidget):
    def __init__(self, mode, parent):
        super(DateTimePopup, self).__init__(parent)
        self.ui = DateTimePopupUi()
        self.ui.setupUi(self)
        self.__mode = mode
        self.__dtHelper = self._getDtHelper()

    @property
    def calendarWidget(self) -> QCalendarWidget:
        """Gets calendar widget from popup.

        Returns:
             QCalendarWidget: Calendar widget.

        """
        return self.ui.calendarWidget

    @calendarWidget.setter
    def calendarWidget(self, calendar):
        """Sets calendar widget from popup.

        Args:
            calendar (): New calendar widget from popup.

        """
        self.ui.calendarWidget = calendar

    @property
    def timeWidget(self) -> QWidget:
        """Gets time widget.

        Returns:
             QWidget: Time widget.

        """
        return self.ui.timeWidget

    @property
    def dtHelper(self) -> QObject:
        """Gets settings for datetime, date or time popup.

        Returns:
             QObject: Settings for datetime, date or time popup.

        """
        return self.__dtHelper

    def initUi(self):
        self.__dtHelper.initUi()

    def _getDtHelper(self):
        mode_class_map = {
            Mode.time.value: CustomTimeHelper,
            Mode.date.value: CustomDateHelper,
            Mode.datetime.value: CustomDateTimeHelper,
        }
        return mode_class_map.get(self.__mode.value, CustomDateTimeHelper)(self)

    def reset(self):
        self.ui.calendarWidget.setSelectedDate(QDate.currentDate())
        self.ui.timeWidget.reset()

    def setToday(self):
        self.ui.calendarWidget.setSelectedDate(QDate.currentDate())
        self.ui.timeWidget.setToday()
