# -*- coding: utf-8 -*-
__all_ = ["CustomDateHelper", "CustomTimeHelper", "CustomDateTimeHelper"]
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from PySide2.QtCore import QTime, QDateTime, QObject, QSize, QRegExp, QDate
from PySide2.QtGui import QRegExpValidator
from PySide2.QtWidgets import QListWidgetItem, QTimeEdit, QDateTimeEdit, QDateEdit


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
        """

        Returns:

        """
        pass

    @abstractmethod
    def getDateTime(self):
        pass

    @abstractmethod
    def setDateTime(self, datetime: Union[QDate, QDateTime, QTime]):
        pass

    @abstractmethod
    def tryConvertDatetime(self, datetime_str: str):
        pass


class CustomDateHelper(AbstractHelper):
    def __init__(self, parent):
        super().__init__(parent)
        self.__parent = parent
        self.__icon = str(
            Path(__file__).resolve().parent
            / r"..\resources\icon\datepicker-widget-icons_calendar.svg"
        )
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
        self.__parent.resize(313, 221)
        self.__parent.calendarWidget.setVisible(True)
        self.__parent.timeWidget.setVisible(False)

    def getDateTime(self):
        return self.__parent.calendarWidget.selectedDate()

    def setDateTime(self, datetime):
        self.__parent.calendarWidget.setSelectedDate(datetime.date())

    def tryConvertDatetime(self, datetime_str):
        try:
            dt = QDate.fromString(datetime_str, self.__format)
            if not dt.isValid():
                return False
            return True
        except:
            return False


class CustomTimeHelper(AbstractHelper):
    def __init__(self, parent):
        super().__init__(parent)
        self.__parent = parent
        self.__icon = str(
            Path(__file__).resolve().parent
            / r"..\resources\icon\datepicker-widget-icons_clock.svg"
        )
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
        self.__parent.resize(300, 221)
        self.__parent.calendarWidget.setVisible(False)
        self.__parent.timeWidget.setVisible(True)

    def getDateTime(self):
        selected_hour = self.__parent.timeWidget.hourListWidget.selectedItems()[0].text()
        selected_min = self.__parent.timeWidget.minListWidget.selectedItems()[0].text()
        selected_sec = self.__parent.timeWidget.secListWidget.selectedItems()[0].text()
        return QTime.fromString(
            f"{selected_hour}:{selected_min}:{selected_sec}", "h:m:s"
        )

    def setDateTime(self, datetime):
        self.__parent.timeWidget.setTime(datetime.time())

    def tryConvertDatetime(self, datetime_str):
        try:
            dt = QTime.fromString(datetime_str, self.__format)
            if not dt.isValid():
                return False
            return True
        except:
            return False


class CustomDateTimeHelper(AbstractHelper):
    def __init__(self, parent):
        super().__init__(parent)
        self.__parent = parent
        self.__icon = str(
            Path(__file__).resolve().parent
            / r"..\resources\icon\datepicker-widget-icons_calendar+clock.svg"
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
        self.__parent.resize(492, 221)
        self.__parent.calendarWidget.setVisible(True)
        self.__parent.timeWidget.setVisible(True)
        self.__parent.timeWidget.setMaximumSize(QSize(170, 182))

    def getDateTime(self):
        selected_date = self.__parent.calendarWidget.selectedDate()
        selected_hour = self.__parent.timeWidget.hourListWidget.selectedItems()[0].text()
        selected_min = self.__parent.timeWidget.minListWidget.selectedItems()[0].text()
        selected_sec = self.__parent.timeWidget.secListWidget.selectedItems()[0].text()
        return QDateTime.fromString(
            f"{selected_date.toString()} {selected_hour}:{selected_min}:{selected_sec}",
            "ddd MMM d yyyy h:m:s",
        )

    def setDateTime(self, datetime):
        self.__parent.calendarWidget.setSelectedDate(datetime.date())
        self.__parent.timeWidget.setTime(datetime.time())

    def tryConvertDatetime(self, datetime_str):
        try:
            dt = QDateTime.fromString(datetime_str, self.__format)
            if not dt.isValid():
                return False
            return True
        except:
            return False
