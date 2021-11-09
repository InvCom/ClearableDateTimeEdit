# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from PySide2.QtCore import QTime, QDateTime, QObject, QSize, QRegExp, QDate
from PySide2.QtGui import QRegExpValidator
from PySide2.QtWidgets import QListWidgetItem, QTimeEdit, QDateTimeEdit, QDateEdit


class AbstractHelper(ABC):
    @abstractmethod
    def init_ui(self):
        pass

    @abstractmethod
    def get_datetime(self):
        pass

    @abstractmethod
    def set_datetime(self, datetime: Union[QDate, QDateTime, QTime]):
        pass

    @abstractmethod
    def try_convert_datetime(self, datetime_str: str):
        pass


class CustomDateHelper(QObject, AbstractHelper):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self._icon = str(
            Path(__file__).resolve().parent
            / r"..\resources\icon\datepicker-widget-icons_calendar.svg"
        )
        self._format = "dd.MM.yyyy"

    @property
    def icon(self) -> str:
        """Gets icon path.

        Returns:
             str: Icon path.

        """
        return self._icon

    @property
    def format(self) -> str:
        """Gets format string.

        Returns:
             str: Format string.

        """
        return self._format

    @format.setter
    def format(self, value: str):
        """Sets format string.

        Args:
            value (str): New value for format string.

        """
        self._format = value

    def init_ui(self):
        self._parent.resize(313, 221)
        self._parent.calendarWidget.setVisible(True)
        self._parent.timeWidget.setVisible(False)

    def get_datetime(self):
        return self._parent.calendarWidget.selectedDate()

    def set_datetime(self, datetime):
        self._parent.calendarWidget.setSelectedDate(datetime.date())

    def try_convert_datetime(self, datetime_str):
        try:
            dt = QDate.fromString(datetime_str, self._format)
            if not dt.isValid():
                return False
            return True
        except:
            return False


class CustomTimeHelper(QObject, AbstractHelper):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self._icon = str(
            Path(__file__).resolve().parent
            / r"..\resources\icon\datepicker-widget-icons_clock.svg"
        )
        self._format = "HH:mm:ss"

    @property
    def icon(self) -> str:
        """Gets icon path.

        Returns:
             str: Icon path.

        """
        return self._icon

    @property
    def format(self) -> str:
        """Gets format string.

        Returns:
             str: Format string.

        """
        return self._format

    @format.setter
    def format(self, value: str):
        """Sets format string.

        Args:
            value (str): New value for format string.

        """
        self._format = value

    def init_ui(self):
        self._parent.resize(300, 221)
        self._parent.calendarWidget.setVisible(False)
        self._parent.timeWidget.setVisible(True)

    def get_datetime(self):
        selected_hour = self._parent.timeWidget.hourListWidget.selectedItems()[0].text()
        selected_min = self._parent.timeWidget.minListWidget.selectedItems()[0].text()
        selected_sec = self._parent.timeWidget.secListWidget.selectedItems()[0].text()
        return QTime.fromString(
            f"{selected_hour}:{selected_min}:{selected_sec}", "h:m:s"
        )

    def set_datetime(self, datetime):
        self._parent.timeWidget.setTime(datetime.time())

    def try_convert_datetime(self, datetime_str):
        try:
            dt = QTime.fromString(datetime_str, self._format)
            if not dt.isValid():
                return False
            return True
        except:
            return False


class CustomDateTimeHelper(QObject, AbstractHelper):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self._icon = str(
            Path(__file__).resolve().parent
            / r"..\resources\icon\datepicker-widget-icons_calendar+clock.svg"
        )
        self._format = "dd.MM.yyyy HH:mm:ss"

    @property
    def icon(self) -> str:
        """Gets icon path.

        Returns:
             str: Icon path.

        """
        return self._icon

    @property
    def format(self) -> str:
        """Gets format string.

        Returns:
             str: Format string.

        """
        return self._format

    @format.setter
    def format(self, value: str):
        """Sets format string.

        Args:
            value (str): New value for format string.

        """
        self._format = value

    def init_ui(self):
        self._parent.resize(492, 221)
        self._parent.calendarWidget.setVisible(True)
        self._parent.timeWidget.setVisible(True)
        self._parent.timeWidget.setMaximumSize(QSize(170, 182))

    def get_datetime(self):
        selected_date = self._parent.calendarWidget.selectedDate()
        selected_hour = self._parent.timeWidget.hourListWidget.selectedItems()[0].text()
        selected_min = self._parent.timeWidget.minListWidget.selectedItems()[0].text()
        selected_sec = self._parent.timeWidget.secListWidget.selectedItems()[0].text()
        return QDateTime.fromString(
            f"{selected_date.toString()} {selected_hour}:{selected_min}:{selected_sec}",
            "ddd MMM d yyyy h:m:s",
        )

    def set_datetime(self, datetime):
        self._parent.calendarWidget.setSelectedDate(datetime.date())
        self._parent.timeWidget.setTime(datetime.time())

    def try_convert_datetime(self, datetime_str):
        try:
            dt = QDateTime.fromString(datetime_str, self._format)
            if not dt.isValid():
                return False
            return True
        except:
            return False
