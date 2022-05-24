# -*- coding: utf-8 -*-
"""This module contains implementation of calendar pop-ups."""
__all__ = ["DateTimePopup"]
from PySide2.QtCore import QObject, QDate
from PySide2.QtWidgets import QWidget, QCalendarWidget

from ClearableDateTimeEdit.Settings import Mode
from ClearableDateTimeEdit.popup.DateTimePopupUi import DateTimePopupUi as _DateTimePopupUi
from ClearableDateTimeEdit.popup.Helpers import CustomTimeHelper, CustomDateTimeHelper, CustomDateHelper, AbstractHelper


class DateTimePopup(QWidget):
    """This class contains functionality of calendar pop-ups."""
    def __init__(self, mode: Mode, parent):
        super(DateTimePopup, self).__init__(parent)
        self.ui = _DateTimePopupUi()
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
        """Initializes calendar pop-ups ui."""
        self.__dtHelper.initUi()

    def _getDtHelper(self) -> AbstractHelper:
        """Gets helper to handle date/time data.

        Returns:
            AbstractHelper (CustomTimeHelper, CustomDateHelper or CustomDateTimeHelper)

        """
        mode_class_map = {
            Mode.time.value: CustomTimeHelper,
            Mode.date.value: CustomDateHelper,
            Mode.datetime.value: CustomDateTimeHelper,
        }
        return mode_class_map.get(self.__mode.value, CustomDateTimeHelper)(self)

    def reset(self):
        """Resets calendar and time widgets."""
        self.ui.calendarWidget.setSelectedDate(QDate.currentDate())
        self.ui.timeWidget.reset()

    def setToday(self):
        """Sets today data and time in calendar and time widgets."""
        self.ui.calendarWidget.setSelectedDate(QDate.currentDate())
        self.ui.timeWidget.setToday()
