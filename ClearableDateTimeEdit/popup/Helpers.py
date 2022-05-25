# -*- coding: utf-8 -*-
"""This module contains date/datetime/time helpers for handling data in calendar pop-up."""
__all_ = ["AbstractHelper", "CustomDateHelper", "CustomTimeHelper", "CustomDateTimeHelper"]
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from PySide2.QtCore import QDate, QDateTime, QObject, QRegExp, QSize, QTime
from PySide2.QtGui import QRegExpValidator
from PySide2.QtWidgets import QDateEdit, QDateTimeEdit, QListWidgetItem, QTimeEdit


class AbstractHelper(QObject):
    """Abstract class with methods handling the settings or date and time inputs depending on DateTimeEdit mode."""

    @property
    @abstractmethod
    def icon(self) -> str:
        """Returns the path of the icon used in the button in DateTimeEdit.

        Returns:
            Path of the icon used in the button in DateTimeEdit.

        """
        pass

    @property
    @abstractmethod
    def format(self) -> str:
        """Returns the format string used for conversion of DateTime, Date and Time strings to
        QDateTime, QDate and QTime objects.

        Returns:
            Format string used for conversion of DateTime, Date and Time strings to QDateTime, QDate and QTime objects.

        """
        pass

    @format.setter
    @abstractmethod
    def format(self, fmt: str):
        """Sets the format string used for conversion of DateTime, Date and Time strings to
        QDateTime, QDate and QTime objects.

        Args:
            fmt: New value for Format string used for conversion of DateTime, Date and Time strings to QDateTime,
                QDate and QTime objects.

        """
        pass

    @abstractmethod
    def initUi(self):
        """Initializes ui."""
        pass

    @abstractmethod
    def getDateTime(self) -> Union[QDate, QDateTime, QTime]:
        """Returns selected datetime, date or time from calendar pop-up depending on DateTimeEdit mode.

        Returns:
            QDateTime: Selected datetime, date or time.

        """
        pass

    @abstractmethod
    def setDateTime(self, datetime: Union[QDate, QDateTime, QTime]):
        """Sets datetime, date or time in calendar pop-up depending on DateTimeEdit mode.

        Args:
            datetime (Union[QDate, QDateTime, QTime]): Datetime, date or time.

        """
        pass

    @abstractmethod
    def tryConvertDatetime(self, datetime_str: str) -> bool:
        """Tries to convert given string into datetime, date or time.

        Notes:
            Conversion depends on the mode of the DateTimeEdit.

        Args:
            datetime_str (str): Datetime, date or time as string.

        Returns:
            True if the conversion is successful, False otherwise.

        """
        pass


class CustomDateHelper(AbstractHelper):
    """Class with methods handling the settings or date inputs depending on date mode."""

    def __init__(self, parent):
        super().__init__(parent)
        self.__parent = parent
        self.__icon = str(Path(__file__).resolve().parent / r"..\resources\icon\datepicker-widget-icons_calendar.svg")
        self.__format = "dd.MM.yyyy"

    @property
    def icon(self) -> str:
        """Gets icon path.

        Returns:
             str: Icon path.

        """
        return self.__icon

    @property
    def format(self) -> str:
        """Gets format string.

        Returns:
             str: Format string.

        """
        return self.__format

    @format.setter
    def format(self, fmt: str):
        """Sets format string.

        Args:
            fmt (str): New value for format string.

        """
        self.__format = fmt

    def initUi(self):
        """Initializes ui."""
        self.__parent.resize(313, 221)
        self.__parent.calendarWidget.setVisible(True)
        self.__parent.timeWidget.setVisible(False)

    def getDateTime(self) -> QDate:
        """Returns selected date from calendar pop-up.

        Returns:
            QDate: Selected date.

        """
        return self.__parent.calendarWidget.selectedDate()

    def setDateTime(self, datetime: QDate):
        """Sets date in calendar pop-up.

        Args:
            datetime (QDate): Date.

        """
        self.__parent.calendarWidget.setSelectedDate(datetime.date())

    def tryConvertDatetime(self, datetime_str: str) -> bool:
        """Tries to convert given string into date.

        Args:
            datetime_str (str): Date as string.

        Returns:
            True if the conversion is successful, False otherwise.

        """
        try:
            dt = QDate.fromString(datetime_str, self.__format)
            if not dt.isValid():
                return False
            return True
        except Exception:
            return False


class CustomTimeHelper(AbstractHelper):
    """Class with methods handling the settings or time inputs depending on time mode."""

    def __init__(self, parent):
        super().__init__(parent)
        self.__parent = parent
        self.__icon = str(Path(__file__).resolve().parent / r"..\resources\icon\datepicker-widget-icons_clock.svg")
        self.__format = "HH:mm:ss"

    @property
    def icon(self) -> str:
        """Gets icon path.

        Returns:
             str: Icon path.

        """
        return self.__icon

    @property
    def format(self) -> str:
        """Gets format string.

        Returns:
             str: Format string.

        """
        return self.__format

    @format.setter
    def format(self, fmt: str):
        """Sets format string.

        Args:
            fmt (str): New value for format string.

        """
        self.__format = fmt

    def initUi(self):
        """Initializes ui."""
        self.__parent.resize(300, 221)
        self.__parent.calendarWidget.setVisible(False)
        self.__parent.timeWidget.setVisible(True)

    def getDateTime(self) -> QTime:
        """Returns selected time from calendar pop-up.

        Returns:
            QTime: Selected time.

        """
        selected_hour = self.__parent.timeWidget.hourListWidget.selectedItems()[0].text()
        selected_min = self.__parent.timeWidget.minListWidget.selectedItems()[0].text()
        selected_sec = self.__parent.timeWidget.secListWidget.selectedItems()[0].text()
        return QTime.fromString(f"{selected_hour}:{selected_min}:{selected_sec}", "h:m:s")

    def setDateTime(self, datetime: QTime):
        """Sets time in calendar pop-up.

        Args:
            datetime (QTime): Time.

        """
        self.__parent.timeWidget.setTime(datetime.time())

    def tryConvertDatetime(self, datetime_str: str) -> bool:
        """Tries to convert given string into time.

        Args:
            datetime_str (str): Time as string.

        Returns:
            True if the conversion is successful, False otherwise.

        """
        try:
            dt = QTime.fromString(datetime_str, self.__format)
            if not dt.isValid():
                return False
            return True
        except Exception:
            return False


class CustomDateTimeHelper(AbstractHelper):
    """Class with methods handling the settings or date and time inputs depending on datetime mode."""

    def __init__(self, parent):
        super().__init__(parent)
        self.__parent = parent
        self.__icon = str(
            Path(__file__).resolve().parent / r"..\resources\icon\datepicker-widget-icons_calendar+clock.svg"
        )
        self.__format = "dd.MM.yyyy HH:mm:ss"

    @property
    def icon(self) -> str:
        """Gets icon path.

        Returns:
             str: Icon path.

        """
        return self.__icon

    @property
    def format(self) -> str:
        """Gets format string.

        Returns:
             str: Format string.

        """
        return self.__format

    @format.setter
    def format(self, fmt: str):
        """Sets format string.

        Args:
            fmt (str): New value for format string.

        """
        self.__format = fmt

    def initUi(self):
        """Initializes ui."""
        self.__parent.resize(492, 221)
        self.__parent.calendarWidget.setVisible(True)
        self.__parent.timeWidget.setVisible(True)
        self.__parent.timeWidget.setMaximumSize(QSize(170, 182))

    def getDateTime(self) -> QDateTime:
        """Returns selected datetime from calendar pop-up.

        Returns:
            QDateTime: Selected datetime.

        """
        selected_date = self.__parent.calendarWidget.selectedDate()
        selected_hour = self.__parent.timeWidget.hourListWidget.selectedItems()[0].text()
        selected_min = self.__parent.timeWidget.minListWidget.selectedItems()[0].text()
        selected_sec = self.__parent.timeWidget.secListWidget.selectedItems()[0].text()
        return QDateTime.fromString(
            f"{selected_date.toString()} {selected_hour}:{selected_min}:{selected_sec}",
            "ddd MMM d yyyy h:m:s",
        )

    def setDateTime(self, datetime: QDateTime):
        """Sets datetime in calendar pop-up.

        Args:
            datetime (QDateTime): Datetime.

        """
        self.__parent.calendarWidget.setSelectedDate(datetime.date())
        self.__parent.timeWidget.setTime(datetime.time())

    def tryConvertDatetime(self, datetime_str: str) -> bool:
        """Tries to convert given string into datetime.

        Args:
            datetime_str (str): Datetime as string.

        Returns:
            True if the conversion is successful, False otherwise.

        """
        try:
            dt = QDateTime.fromString(datetime_str, self.__format)
            if not dt.isValid():
                return False
            return True
        except Exception:
            return False
