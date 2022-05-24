# -*- coding: utf-8 -*-
"""The module contains the implementation of the DataTimeEdit widget."""

__all__ = ["ClearableDateTimeEdit"]

from typing import Union

from PySide2 import QtCore, QtGui
from PySide2.QtCore import QDate, QDateTime, Qt, QTime
from PySide2.QtGui import QFocusEvent, QKeyEvent, QResizeEvent
from PySide2.QtWidgets import (
    QCalendarWidget,
    QDateTimeEdit,
    QLineEdit,
    QStyle,
    QToolButton,
)

from ClearableDateTimeEdit.popup import DateTimePopup, TimeWidget
from ClearableDateTimeEdit.Settings import Mode


class ClearableDateTimeEdit(QLineEdit):
    """ClearableDateTimeEdit contains the implementation of the DateTimeEdit widget, with which date, datetime or time
    can be selected or entered manually and also cleared again."""

    dateChanged = QtCore.Signal(object)
    dateTimeChanged = QtCore.Signal(object)
    editingFinished = QtCore.Signal(object)
    timeChanged = QtCore.Signal(object)

    def __init__(self, parent=None, mode: Mode = Mode.datetime):
        super(ClearableDateTimeEdit, self).__init__(parent)
        self.__mode = mode
        self.__showPopup = True
        self.__popup = DateTimePopup(self.__mode, self)
        self.__dateTimeText = ""
        self.__dateTimeEdit = QDateTimeEdit()
        self.__dateTimeEdit.setDisplayFormat(self.__popup.dtHelper.format)
        self.__popupBtn = QToolButton(self)
        self.__initUi()

    def __initUi(self):
        """Performs ui settings."""
        self.__popupBtn.setStyleSheet("border: 0px; padding: 0px;")
        self.__popupBtn.setCursor(QtCore.Qt.ArrowCursor)
        self.__popupBtn.setIcon(QtGui.QIcon(self.__popup.dtHelper.icon))
        self.setCalendarPopup(self.__showPopup)

        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        buttonSize = self.__popupBtn.sizeHint()

        self.setStyleSheet("QLineEdit {padding-right: %dpx; }" % (buttonSize.width() + frameWidth + 1))
        self.setMinimumSize(
            max(self.minimumSizeHint().width(), buttonSize.width() + frameWidth * 2 + 2),
            max(self.minimumSizeHint().height(), buttonSize.height() + frameWidth * 2 + 2),
        )
        self.__popup.ui.submitButton.clicked.connect(self.__submit)
        self.__popup.ui.cancelButton.clicked.connect(self.__close)
        self.__popup.ui.nowButton.clicked.connect(self.__setToday)
        self.__popup.ui.clearButton.clicked.connect(self.__clear)

    def resizeEvent(self, event: QResizeEvent):
        """Moves pop-up button to the right place during the resize event.

        Args:
            event (QResizeEvent): Resize event.

        """
        buttonSize = self.__popupBtn.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.__popupBtn.move(
            self.rect().right() - frameWidth - buttonSize.width(),
            (self.rect().bottom() - buttonSize.height() + 1) / 2,
        )
        super(ClearableDateTimeEdit, self).resizeEvent(event)

    def __openCalendar(self):
        """Moves the custom calendar widget to the left side of LineEdit and shows it."""
        point = self.rect().bottomRight()
        global_point = self.mapToGlobal(point)
        self.__popup.move(global_point - QtCore.QPoint(self.width(), 0))
        self.__popup.show()

    def __clear(self):
        """Removes the data entered in the LineEdit."""
        self.clear()
        self.__popup.reset()
        self.__popup.close()
        self.__dateTimeText = ""
        self.dateTimeChanged.emit(None)

    def __setToday(self):
        """Sets today's date/time in the LineEdit."""
        self.__popup.setToday()
        self.__submit()

    def __submit(self):
        """Validates the date/time selected in the calendar, inserts it into the LineEdit and closes the calendar
        widget.
        """
        dt = self.__popup.dtHelper.getDateTime()
        dt_text = dt.toString(self.__popup.dtHelper.format)
        is_valid = self.__dateTimeEdit.validate(dt_text, 0)
        if is_valid[0] == QtGui.QValidator.State.Invalid:
            dt_type = str(type(dt)).split("'")[1]
            raise ValueError(f"'{self.__popup.dtHelper.format}' is not acceptable format for '{dt_type}'")
        self.setText(dt_text)
        self.__popup.close()
        self.__dateTimeEdit.setDateTime(self.__dateTimeEdit.dateTimeFromText(dt_text))
        self.dateTimeChanged.emit(self.__dateTimeEdit.dateTime())
        self.__checkAndSendSignal(
            self.__dateTimeEdit.dateTimeFromText(self.__dateTimeText), self.__dateTimeEdit.dateTime()
        )
        self.__dateTimeText = dt_text

    def __close(self):
        """Closes the calendar widget."""
        self.__popup.hide()

    def __checkAndSendSignal(self, old_dt: QDateTime, new_dt: QDateTime):
        """Sends a signal with a date if the date of the DateTime parameter passed is different. Sends a signal with
        time if the time of the DateTime parameter is different.

        Args:
            old_dt (QDateTime): First QDateTime.
            new_dt (QDateTime): Second QDateTime.

        """
        if not old_dt.date() == new_dt.date():
            self.dateChanged.emit(new_dt.date())
        if not old_dt.time() == new_dt.time():
            self.timeChanged.emit(new_dt.time())

    def focusOutEvent(self, event: QFocusEvent):
        """Takes over the entries in LineEdit when the focus is lost if the entries have been changed.

        Args:
            event (QFocusEvent): QFocusEvent.

        """
        if self.text() != self.__dateTimeText:
            self.__editingFinished()
        super(ClearableDateTimeEdit, self).focusOutEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        """Takes over the entries in LineEdit when enter pressed.

        Args:
            event (QKeyEvent): QKeyEvent.

        """
        if event.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            self.__editingFinished()
        super(ClearableDateTimeEdit, self).keyPressEvent(event)

    def __editingFinished(self):
        """Takes over the entries in LineEdit."""
        if not self.text():
            self.editingFinished.emit(None)
            self.__dateTimeText = ""
        else:
            dt_valid = self.__dateTimeEdit.validate(self.text(), 0)
            if dt_valid[0] in [QtGui.QValidator.State.Acceptable, QtGui.QValidator.State.Intermediate]:
                fixed_dt = self.__dateTimeEdit.fixup(dt_valid[1])
                if self.__popup.dtHelper.tryConvertDatetime(fixed_dt):
                    dt = self.__dateTimeEdit.dateTimeFromText(fixed_dt)
                    self.__dateTimeEdit.setDateTime(dt)
                    self.__popup.dtHelper.setDateTime(dt)
                    self.editingFinished.emit(self.__popup.dtHelper.getDateTime())
                    self.dateTimeChanged.emit(dt)
                    self.__checkAndSendSignal(
                        self.__dateTimeEdit.dateTimeFromText(self.__dateTimeText), self.__dateTimeEdit.dateTime()
                    )
                    self.__dateTimeText = fixed_dt
            self.setText(self.__dateTimeText)

    def timeWidget(self) -> TimeWidget:
        """Returns the time widget used in pop-up.

        Returns:
            Time widget used in pop-up.

        """
        return self.__popup.ui.timeWidget

    def calendar(self):
        raise NotImplementedError("Not implemented yet")

    def calendarPopup(self) -> bool:
        """Returns current calendar pop-up show mode.

        Returns:
            Current calendar pop-up show mode.

        """
        return self.__showPopup

    def calendarWidget(self) -> QCalendarWidget:
        """Returns the calendar widget used in calendar pop-up.

        Returns:
            Calendar widget used in calendar pop-up.

        """
        return self.__popup.calendarWidget

    def clearMaximumDate(self):
        """Resets maximum date in calendar widget."""
        self.__dateTimeEdit.clearMaximumDate()
        max_date = self.__dateTimeEdit.maximumDate()
        self.__popup.calendarWidget.setMaximumDate(max_date)

    def clearMaximumDateTime(self):
        """Resets maximum date in calendar widget and maximum time in time widget."""
        self.__dateTimeEdit.clearMaximumDateTime()
        max_date = self.__dateTimeEdit.maximumDate()
        self.__popup.calendarWidget.setMaximumDate(max_date)
        self.__popup.timeWidget.clearMaximumTime()

    def clearMaximumTime(self):
        """Resets maximum time in time widget."""
        self.__dateTimeEdit.clearMaximumTime()
        self.__popup.timeWidget.clearMaximumTime()

    def clearMinimumDate(self):
        """Resets minimum date in calendar widget."""
        self.__dateTimeEdit.clearMinimumDate()
        min_date = self.__dateTimeEdit.minimumDate()
        self.__popup.calendarWidget.setMinimumDate(min_date)

    def clearMinimumDateTime(self):
        """Resets minimum date in calendar widget and minimum time in time widget."""
        self.__dateTimeEdit.clearMinimumDateTime()
        min_date = self.__dateTimeEdit.maximumDate()
        self.__popup.calendarWidget.setMinimumDate(min_date)
        self.__popup.timeWidget.clearMinimumTime()

    def clearMinimumTime(self):
        """Resets minimum time in time widget."""
        self.__dateTimeEdit.clearMinimumTime()
        self.__popup.timeWidget.clearMinimumTime()

    def currentSection(self):
        raise NotImplementedError("Not implemented yet")

    def currentSectionIndex(self):
        raise NotImplementedError("Not implemented yet")

    def date(self) -> Union[QDate, None]:
        """Gets current selected date or None if line edit is empty.

        Returns:
            Union[QDate, None]: Current selected date or None if line edit is empty.

        """
        if not self.__dateTimeText:
            return None
        else:
            return self.__dateTimeEdit.date()

    def dateTime(self) -> Union[QDateTime, None]:
        """Gets current selected datetime or None if LineEdit is empty.

        Returns:
            Union[QDateTime, None]: Current selected datetime or None if LineEdit is empty.

        """
        if not self.__dateTimeText:
            return None
        else:
            return self.__dateTimeEdit.dateTime()

    def displayFormat(self) -> str:
        """Gets current display format.

        Returns:
            String: Current display format.

        """
        return self.__popup.dtHelper.format

    def dateTimeFromText(self, text: str) -> QDateTime:
        """Converts given text in QDateTime.

        Args:
            text (str): Text to be convert in QDateTime.

        Raises:
            TypeError if given test is not string.

        Returns:
            QDateTime from given text.

        """
        if not isinstance(text, str):
            text_type = str(type(text)).split("'")[1]
            raise TypeError(
                f"""'DateTimeEdit.dateTimeFromText' called with wrong argument types:\n\t
                DateTimeEdit.dateTimeFromText({text_type})\n\t\t
                Supported signatures:\n\t
                DateTimeEdit.dateTimeFromText(str)"""
            )
        return self.__dateTimeEdit.dateTimeFromText(text)

    def displayedSections(self):
        raise NotImplementedError("Not implemented yet")

    def maximumDate(self) -> QDate:
        """Gets maximum date as QDate.

        Returns:
            QDate: Maximum date.

        """
        return self.__popup.calendarWidget.maximumDate()

    def maximumDateTime(self) -> QDateTime:
        """Gets maximum datetime as QDateTime.

        Returns:
            QDateTime: Maximum datetime.

        """
        return self.__dateTimeEdit.maximumDateTime()

    def maximumTime(self) -> QTime:
        """Gets maximum time as QTime.

        Returns:
            QTime: Maximum time.

        """
        return self.__popup.timeWidget.maximumTime()

    def minimumDate(self) -> QDate:
        """Gets minimum date as QDate.

        Returns:
            QDate: Minimum date.

        """
        return self.__popup.calendarWidget.minimumDate()

    def minimumDateTime(self) -> QDateTime:
        """Gets minimum datetime as QDateTime.

        Returns:
            QDateTime: Minimum datetime.

        """
        return self.__dateTimeEdit.minimumDateTime()

    def minimumTime(self) -> QTime:
        """Gets minimum time as QTime.

        Returns:
            QTime: Minimum time.

        """
        return self.__popup.timeWidget.minimumTime()

    def mode(self) -> Mode:
        """Gets current mode of DateTimeEdit as enum "Mode". Possible is Mode.date, Mode.datetime or Mode.time.

        Returns:
            Mode: Current mode as enum "Mode".

        """
        return self.__mode

    def sectionAt(self, index):
        raise NotImplementedError("Not implemented yet")

    def sectionCount(self):
        raise NotImplementedError("Not implemented yet")

    def sectionText(self, section):
        raise NotImplementedError("Not implemented yet")

    def setCalendar(self, calendar):
        raise NotImplementedError("Not implemented yet")

    def setCalendarPopup(self, enable: bool):
        """Enables the activation of calendar pop-up.

        Args:
            enable (bool): Flag to enable calendar pop-up. If flag is True, pop-up is activated, otherwise deactivated.

        """
        self.__showPopup = enable
        if self.__showPopup:
            self.__popupBtn.setEnabled(True)
            self.__popup.initUi()
            self.__popupBtn.clicked.connect(self.__openCalendar)
        else:
            self.__popupBtn.setEnabled(False)

    def setCalendarWidget(self, calendarWidget: QCalendarWidget):
        """Sets the given calendarWidget as the widget to be used for the calendar pop-up.

        Args:
            calendarWidget (QCalendarWidget): QCalendarWidget.

        """
        self.__dateTimeEdit.setCalendarWidget(calendarWidget)
        self.__popup.calendarWidget = calendarWidget

    def setCurrentSection(self, section):
        raise NotImplementedError("Not implemented yet")

    def setCurrentSectionIndex(self, index):
        raise NotImplementedError("Not implemented yet")

    def setDate(self, date: QDate):
        """Sets given date in calendar pop-up and line edit.

        Args:
            date (QDate): Given date.

        Raises:
            TypeError if given date is not QDate.

        """
        if not isinstance(date, QDate):
            date_type = str(type(date)).split("'")[1]
            raise TypeError(
                f"""'DateTimeEdit.setDate' called with wrong argument types:\n\t
                DateTimeEdit.setDate({date_type})\n\t\t
                Supported signatures:\n\t
                DateTimeEdit.setDate(PySide2.QtCore.QDate)"""
            )
        self.__dateTimeEdit.setDate(date)
        self.__popup.calendarWidget.setSelectedDate(date)
        self.setText(date.toString(self.__popup.dtHelper.format))

    def setDateRange(self, min: QDate, max: QDate):
        """Sets minimum and maximum dates.

        Args:
            min (QDate): Minimum date.
            max (QDate): Maximum date.

        Raises:
            TypeError if given minimum or maximum date not QDate.

        """
        if not isinstance(min, QDate):
            min_type = str(type(min)).split("'")[1]
            raise TypeError(
                f"""'DateTimeEdit.setDateRange' called with wrong argument types:\n\t
                DateTimeEdit.setDateRange({min_type})\n\t\t
                Supported signatures:\n\t
                DateTimeEdit.setDateRange(PySide2.QtCore.QDate)"""
            )
        if not isinstance(max, QDateTime):
            max_type = str(type(max)).split("'")[1]
            raise TypeError(
                f"""'DateTimeEdit.setDateRange' called with wrong argument types:\n\t
                DateTimeEdit.setDateRange({max_type})\n\t\t
                Supported signatures:\n\t
                DateTimeEdit.setDateRange(PySide2.QtCore.QDate)"""
            )
        self.setMinimumDate(min)
        self.setMaximumDate(max)

    def setDateTime(self, dt: QDateTime):
        """Sets given datetime in calendar pop-up, time widget and line edit.

        Args:
            dt (QDateTime): Given datetime.

        Raises:
            TypeError if given datetime is not QDateTime.

        """
        if not isinstance(dt, QDateTime):
            dt_type = str(type(dt)).split("'")[1]
            raise TypeError(
                f"""'DateTimeEdit.setDateTime' called with wrong argument types:\n\t
                DateTimeEdit.setDateTime({dt_type})\n\t\t
                Supported signatures:\n\t
                DateTimeEdit.setDateTime(PySide2.QtCore.QDateTime)"""
            )
        self.__dateTimeEdit.setDateTime(dt)
        self.__popup.calendarWidget.setSelectedDate(dt.date())
        self.__popup.timeWidget.setTime(dt.time())
        self.setText(dt.toString(self.__popup.dtHelper.format))

    def setDateTimeRange(self, min: QDateTime, max: QDateTime):
        """Sets minimum and maximum datetime.

        Args:
            min (QDateTime): Minimum date.
            max (QDateTime): Maximum date.

        Raises:
            TypeError if given minimum or maximum datetime is not QDateTime.

        """
        if not isinstance(min, QDateTime):
            min_type = str(type(min)).split("'")[1]
            raise TypeError(
                f"""'DateTimeEdit.setDateTimeRange' called with wrong argument types:\n\t
                DateTimeEdit.setDateTimeRange({min_type})\n\t\t
                Supported signatures:\n\t
                DateTimeEdit.setDateTimeRange(PySide2.QtCore.QDateTime)"""
            )
        if not isinstance(max, QDateTime):
            max_type = str(type(max)).split("'")[1]
            raise TypeError(
                f"""'DateTimeEdit.setDateTimeRange' called with wrong argument types:\n\t
                DateTimeEdit.setDateTimeRange({max_type})\n\t\t
                Supported signatures:\n\t
                DateTimeEdit.setDateTimeRange(PySide2.QtCore.QDateTime)"""
            )
        self.setMinimumDateTime(min)
        self.setMaximumDateTime(max)

    def setDisplayFormat(self, format: str):
        """Sets the display format.

        Args:
            format (str): New display format.

        """
        self.__dateTimeEdit.setDisplayFormat(format)
        self.__popup.dtHelper.format = format

    def setMaximumDate(self, max: QDate):
        """Sets maximum date in calendar pop-up.

        Args:
            max (QDate): Maximum date as QDate.

        """
        self.__dateTimeEdit.setMaximumDate(max)
        self.__popup.calendarWidget.setMaximumDate(max)

    def setMaximumDateTime(self, dt: QDateTime):
        """Sets maximum date in calendar pop-up and maximum time in time widget.

        Args:
            dt (QDateTime): Maximum datetime as QDateTime.

        """
        self.__dateTimeEdit.setMaximumDateTime(dt)
        self.__popup.calendarWidget.setMaximumDate(dt.date())
        self.__popup.timeWidget.setMaximumTime(dt.time())

    def setMaximumTime(self, max: QTime):
        """Sets maximum time in time widget.

        Args:
            max (QTime): Maximum time as QTime.

        """
        self.__dateTimeEdit.setMaximumTime(max)
        self.__popup.timeWidget.setMaximumTime(max)

    def setMinimumDate(self, min: QDate):
        """Sets minimum date in calendar pop-up.

        Args:
            min (QDate): Minimum date as QDate.

        """
        self.__dateTimeEdit.setMinimumDate(min)
        self.__popup.calendarWidget.setMinimumDate(min)

    def setMinimumDateTime(self, dt: QDateTime):
        """Sets minimum date in calendar pop-up and minimum time in time widget.

        Args:
            dt (QDateTime): Minimum datetime as QDateTime.

        """
        self.__dateTimeEdit.setMinimumDateTime(dt)
        self.__popup.calendarWidget.setMinimumDate(dt.date())
        self.__popup.timeWidget.setMinimumTime(dt.time())

    def setMinimumTime(self, min: QTime):
        """Sets minimum time in time widget.

        Args:
            min (QTime): Minimum time as QTime.

        """
        self.__dateTimeEdit.setMinimumTime(min)
        self.__popup.timeWidget.setMinimumTime(min)

    def setMode(self, mode: Mode):
        """Sets mode of DateTimeEdit. Possible is Mode.date, Mode.datetime or Mode.time.

        Args:
            mode (Mode): Mode as enum "Mode".

        Raises:
            TypeError if the type of given mode is not Mode.

        """
        if not isinstance(mode, Mode):
            mode_type = str(type(mode)).split("'")[1]
            raise TypeError(
                f"""'DateTimeEdit.setMode' called with wrong argument types:\n\t
                DateTimeEdit.setMode({mode_type})\n\t\t
                Supported signatures:\n\t
                DateTimeEdit.setMode(Mode)"""
            )
        self.__mode = mode
        self.__popup = DateTimePopup(self.__mode, self)
        self.__popupBtn.setIcon(QtGui.QIcon(self.__popup.dtHelper.icon))

    def setSelectedSection(self, section):
        raise NotImplementedError("Not implemented yet")

    def setTime(self, time: QTime):
        """Sets given time in time widget and line edit.

        Args:
            time (QTime): Given time.

        Raises:
            TypeError if given time is not QTime.

        """
        if not isinstance(time, QTime):
            time_type = str(type(time)).split("'")[1]
            raise TypeError(
                f"""'DateTimeEdit.setTime' called with wrong argument types:\n\t
                DateTimeEdit.setTime({time_type})\n\t\t
                Supported signatures:\n\t
                DateTimeEdit.setTime(PySide2.QtCore.QTime)"""
            )
        self.__dateTimeEdit.setTime(time)
        self.__popup.timeWidget.setTime(time)
        self.setText(time.toString(self.__popup.dtHelper.format))

    def setTimeRange(self, min: QTime, max: QTime):
        """Sets minimum and maximum time.

        Args:
            min (QTime): Minimum time.
            max (QTime): Maximum time.

        """
        self.setMinimumTime(min)
        self.setMaximumTime(max)

    def setTimeSpec(self, spec: Qt.TimeSpec):
        """Sets the time specification used in this datetime to spec.

        Args:
            spec (Qt.TimeSpec): New time specification.

        """
        self.__dateTimeEdit.setTimeSpec(spec)

    def textFromDateTime(self, dt: QDateTime) -> str:
        """Converts given datetime in string.

        Args:
            dt (QDateTime): Datetime.

        Returns:
            Datetime as string.

        """
        return self.__dateTimeEdit.textFromDateTime(dt)

    def time(self) -> Union[QTime, None]:
        """Gets current selected time or None if line edit is empty.

        Returns:
            Union[QTime, None]: Current selected time or None if LineEdit is empty.

        """
        if not self.__dateTimeText:
            return None
        else:
            return self.__dateTimeEdit.time()

    def timeSpec(self) -> Qt.TimeSpec:
        """Returns the time specification of the datetime.

        Returns:
            Qt.TimeSpec: Time specification.

        """
        return self.__dateTimeEdit.timeSpec()
