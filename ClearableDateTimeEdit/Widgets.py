# -*- coding: utf-8 -*-

__all__ = ["ClearableDateTimeEdit"]

from PySide2 import QtCore, QtGui
from PySide2.QtCore import QDate, QDateTime, QTime
from PySide2.QtWidgets import QToolButton, QStyle, QCalendarWidget, QLineEdit, QDateTimeEdit

from ClearableDateTimeEdit.Settings import Mode
from ClearableDateTimeEdit.popup import DateTimePopup
from ClearableDateTimeEdit.popup import TimeWidget


class ClearableDateTimeEdit(QLineEdit):

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

        self.setStyleSheet(
            "QLineEdit {padding-right: %dpx; }" % (buttonSize.width() + frameWidth + 1)
        )
        self.setMinimumSize(
            max(
                self.minimumSizeHint().width(), buttonSize.width() + frameWidth * 2 + 2
            ),
            max(
                self.minimumSizeHint().height(), buttonSize.height() + frameWidth * 2 + 2
            ),
        )
        self.__popup.ui.submitButton.clicked.connect(self.__submit)
        self.__popup.ui.cancelButton.clicked.connect(self.__close)
        self.__popup.ui.nowButton.clicked.connect(self.__setToday)
        self.__popup.ui.clearButton.clicked.connect(self.__clear)

    def resizeEvent(self, event):
        buttonSize = self.__popupBtn.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.__popupBtn.move(
            self.rect().right() - frameWidth - buttonSize.width(),
            (self.rect().bottom() - buttonSize.height() + 1) / 2,
        )
        super(ClearableDateTimeEdit, self).resizeEvent(event)

    def __openCalendar(self):
        point = self.rect().bottomRight()
        global_point = self.mapToGlobal(point)
        self.__popup.move(global_point - QtCore.QPoint(self.width(), 0))
        self.__popup.show()

    def __clear(self):
        self.clear()
        self.__popup.reset()
        self.__popup.close()
        self.__dateTimeText = ""
        self.dateTimeChanged.emit(None)

    def __setToday(self):
        self.__popup.setToday()
        self.__submit()

    def __submit(self):
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
        self.__checkAndSendSignal(self.__dateTimeEdit.dateTimeFromText(self.__dateTimeText), self.__dateTimeEdit.dateTime())
        self.__dateTimeText = dt_text

    def __close(self):
        self.__popup.hide()

    def __checkAndSendSignal(self, old_dt, new_dt):
        if not old_dt.date() == new_dt.date():
            self.dateChanged.emit(new_dt.date())
        if not old_dt.time() == new_dt.time():
            self.timeChanged.emit(new_dt.time())

    def focusOutEvent(self, event):
        if self.text() != self.__dateTimeText:
            self.__editingFinished()
        super(ClearableDateTimeEdit, self).focusOutEvent(event)

    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            self.__editingFinished()
        super(ClearableDateTimeEdit, self).keyPressEvent(event)

    def __editingFinished(self):
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
                    self.__checkAndSendSignal(self.__dateTimeEdit.dateTimeFromText(self.__dateTimeText), self.__dateTimeEdit.dateTime())
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
        self.__dateTimeEdit.clearMaximumDate()
        max_date = self.__dateTimeEdit.maximumDate()
        self.__popup.calendarWidget.setMaximumDate(max_date)

    def clearMaximumDateTime(self):
        self.__dateTimeEdit.clearMaximumDateTime()
        max_date = self.__dateTimeEdit.maximumDate()
        self.__popup.calendarWidget.setMaximumDate(max_date)
        self.__popup.timeWidget.clearMaximumTime()

    def clearMaximumTime(self):
        self.__dateTimeEdit.clearMaximumTime()
        self.__popup.timeWidget.clearMaximumTime()

    def clearMinimumDate(self):
        self.__dateTimeEdit.clearMinimumDate()
        min_date = self.__dateTimeEdit.minimumDate()
        self.__popup.calendarWidget.setMinimumDate(min_date)

    def clearMinimumDateTime(self):
        self.__dateTimeEdit.clearMinimumDateTime()
        min_date = self.__dateTimeEdit.maximumDate()
        self.__popup.calendarWidget.setMinimumDate(min_date)
        self.__popup.timeWidget.clearMinimumTime()

    def clearMinimumTime(self):
        self.__dateTimeEdit.clearMinimumTime()
        self.__popup.timeWidget.clearMinimumTime()

    def currentSection(self):
        raise NotImplementedError("Not implemented yet")

    def currentSectionIndex(self):
        raise NotImplementedError("Not implemented yet")

    def date(self):
        if not self.__dateTimeText:
            return None
        else:
            return self.__dateTimeEdit.date()

    def dateTime(self):
        if not self.__dateTimeText:
            return None
        else:
            return self.__dateTimeEdit.dateTime()

    def displayFormat(self):
        return self.__popup.dtHelper.format

    def dateTimeFromText(self, text: str):
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

    def maximumDate(self):
        return self.__popup.calendarWidget.maximumDate()

    def maximumDateTime(self):
        return self.__dateTimeEdit.maximumDateTime()

    def maximumTime(self):
        return self.__popup.timeWidget.maximumTime()

    def minimumDate(self):
        return self.__popup.calendarWidget.minimumDate()

    def minimumDateTime(self):
        return self.__dateTimeEdit.minimumDateTime()

    def minimumTime(self):
        return self.__popup.timeWidget.minimumTime()

    def mode(self):
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
        self.__showPopup = enable
        if self.__showPopup:
            self.__popupBtn.setEnabled(True)
            self.__popup.initUi()
            self.__popupBtn.clicked.connect(self.__openCalendar)
        else:
            self.__popupBtn.setEnabled(False)

    def setCalendarWidget(self, calendarWidget):
        self.__dateTimeEdit.setCalendarWidget(calendarWidget)
        self.__popup.calendarWidget = calendarWidget

    def setCurrentSection(self, section):
        raise NotImplementedError("Not implemented yet")

    def setCurrentSectionIndex(self, index):
        raise NotImplementedError("Not implemented yet")

    def setDate(self, date: QDate):
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

    def setDateTimeRange(self, min, max):
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

    def setDisplayFormat(self, format):
        self.__dateTimeEdit.setDisplayFormat(format)
        self.__popup.dtHelper.format = format

    def setMaximumDate(self, max):
        self.__dateTimeEdit.setMaximumDate(max)
        self.__popup.calendarWidget.setMaximumDate(max)

    def setMaximumDateTime(self, dt):
        self.__dateTimeEdit.setMaximumDateTime(dt)
        self.__popup.calendarWidget.setMaximumDate(dt.date())
        self.__popup.timeWidget.setMaximumTime(dt.time())

    def setMaximumTime(self, max):
        self.__dateTimeEdit.setMaximumTime(max)
        self.__popup.timeWidget.setMaximumTime(max)

    def setMinimumDate(self, min):
        self.__dateTimeEdit.setMinimumDate(min)
        self.__popup.calendarWidget.setMinimumDate(min)

    def setMinimumDateTime(self, dt):
        self.__dateTimeEdit.setMinimumDateTime(dt)
        self.__popup.calendarWidget.setMinimumDate(dt.date())
        self.__popup.timeWidget.setMinimumTime(dt.time())

    def setMinimumTime(self, min):
        self.__dateTimeEdit.setMinimumTime(min)
        self.__popup.timeWidget.setMinimumTime(min)

    def setMode(self, mode: Mode):
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

    def setTimeRange(self, min, max):
        self.setMinimumTime(min)
        self.setMaximumTime(max)

    def setTimeSpec(self, spec):
        self.__dateTimeEdit.setTimeSpec(spec)

    def textFromDateTime(self, dt):
        self.__dateTimeEdit.textFromDateTime(dt)

    def time(self):
        if not self.__dateTimeText:
            return None
        else:
            return self.__dateTimeEdit.time()

    def timeSpec(self):
        return self.__dateTimeEdit.timeSpec()
