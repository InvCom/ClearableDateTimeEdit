# -*- coding: utf-8 -*-
from datetime import datetime

from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import QDate, QDateTime, QTime
from PySide2.QtWidgets import QToolButton, QStyle, QListWidgetItem, QCalendarWidget, QLineEdit, QDateTimeEdit, QWidget

# from resources.calender_popup import Ui_Form
from date_time_edit.popup.classes import CustomTimeHelper, CustomDateHelper, CustomDateTimeHelper
from date_time_edit.popup.dt_popup_view import DateTimePopup
from date_time_edit.popup.time_widget import TimeWidget
from date_time_edit.settings import Mode


class DateTimeEdit(QLineEdit):

    dateChanged = QtCore.Signal(object)
    dateTimeChanged = QtCore.Signal(object)
    editingFinished = QtCore.Signal(object)
    timeChanged = QtCore.Signal(object)

    def __init__(self, parent=None, mode: Mode = Mode.datetime):
        super(DateTimeEdit, self).__init__(parent)
        self._mode = mode
        self._show_popup = True
        self._popup = DateTimePopup(self._mode, self)
        self._datetime_text = ""
        self._datetime_edit = QDateTimeEdit()
        self._datetime_edit.setDisplayFormat(self._popup.custom_datetime_settings.format)
        self._popup_btn = QToolButton(self)
        self._initUi()

    def _initUi(self):
        """Performss ui settings."""
        self._popup_btn.setStyleSheet("border: 0px; padding: 0px;")
        self._popup_btn.setCursor(QtCore.Qt.ArrowCursor)
        self._popup_btn.setIcon(QtGui.QIcon(self._popup.custom_datetime_settings.icon))
        self.setCalendarPopup(self._show_popup)

        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        buttonSize = self._popup_btn.sizeHint()

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
        self._popup.ui.submitButton.clicked.connect(self._submit)
        self._popup.ui.cancelButton.clicked.connect(self._close)
        self._popup.ui.nowButton.clicked.connect(self._setToday)
        self._popup.ui.clearButton.clicked.connect(self._clear)

    def resizeEvent(self, event):
        buttonSize = self._popup_btn.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self._popup_btn.move(
            self.rect().right() - frameWidth - buttonSize.width(),
            (self.rect().bottom() - buttonSize.height() + 1) / 2,
        )
        super(DateTimeEdit, self).resizeEvent(event)

    def _openCalendar(self):
        point = self.rect().bottomRight()
        global_point = self.mapToGlobal(point)
        self._popup.move(global_point - QtCore.QPoint(self.width(), 0))
        self._popup.show()

    def _clear(self):
        self.clear()
        self._popup.reset()
        self._popup.close()
        self._datetime_text = ""
        self.dateTimeChanged.emit(None)

    def _setToday(self):
        self._popup.set_today()
        self._submit()

    def _submit(self):
        dt = self._popup.custom_datetime_settings.get_datetime()
        dt_text = dt.toString(self._popup.custom_datetime_settings.format)
        is_valid = self._datetime_edit.validate(dt_text, 0)
        if is_valid[0] == QtGui.QValidator.State.Invalid:
            dt_type = str(type(dt)).split("'")[1]
            raise ValueError(f"'{self._popup.custom_datetime_settings.format}' is not acceptable format for '{dt_type}'")
        self.setText(dt_text)
        self._popup.close()
        self._datetime_edit.setDateTime(self._datetime_edit.dateTimeFromText(dt_text))
        self.dateTimeChanged.emit(self._datetime_edit.dateTime())
        self._checkAndSendSignal(self._datetime_edit.dateTimeFromText(self._datetime_text), self._datetime_edit.dateTime())
        self._datetime_text = dt_text

    def _close(self):
        self._popup.hide()

    def _checkAndSendSignal(self, old_dt, new_dt):
        if not old_dt.date() == new_dt.date():
            self.dateChanged.emit(new_dt.date())
        if not old_dt.time() == new_dt.time():
            self.timeChanged.emit(new_dt.time())

    def focusOutEvent(self, event):
        if self.text() != self._datetime_text:
            self._editingFinished()
        super(DateTimeEdit, self).focusOutEvent(event)

    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            self._editingFinished()
        super(DateTimeEdit, self).keyPressEvent(event)

    def _editingFinished(self):
        if not self.text():
            self.editingFinished.emit(None)
            self._datetime_text = ""
        else:
            dt_valid = self._datetime_edit.validate(self.text(), 0)
            if dt_valid[0] in [QtGui.QValidator.State.Acceptable, QtGui.QValidator.State.Intermediate]:
                fixed_dt = self._datetime_edit.fixup(dt_valid[1])
                if self._popup.custom_datetime_settings.try_convert_datetime(fixed_dt):
                    dt = self._datetime_edit.dateTimeFromText(fixed_dt)
                    self._datetime_edit.setDateTime(dt)
                    self._popup.custom_datetime_settings.set_datetime(dt)
                    self.editingFinished.emit(self._popup.custom_datetime_settings.get_datetime())
                    self.dateTimeChanged.emit(dt)
                    self._checkAndSendSignal(self._datetime_edit.dateTimeFromText(self._datetime_text), self._datetime_edit.dateTime())
                    self._datetime_text = fixed_dt
            self.setText(self._datetime_text)

    def timeWidget(self) -> TimeWidget:
        """Returns the time widget used in pop-up.

        Returns:
            Time widget used in pop-up.

        """
        return self._popup.ui.timeWidget

    def calendar(self):
        raise NotImplementedError("Not implemented yet")

    def calendarPopup(self) -> bool:
        """Returns current calendar pop-up show mode.

        Returns:
            Current calendar pop-up show mode.

        """
        return self._show_popup

    def calendarWidget(self) -> QCalendarWidget:
        """Returns the calendar widget used in calendar pop-up.

        Returns:
            Calendar widget used in calendar pop-up.

        """
        return self._popup.calendarWidget

    def clearMaximumDate(self):
        self._datetime_edit.clearMaximumDate()
        max_date = self._datetime_edit.maximumDate()
        self._popup.calendarWidget.setMaximumDate(max_date)

    def clearMaximumDateTime(self):
        self._datetime_edit.clearMaximumDateTime()
        max_date = self._datetime_edit.maximumDate()
        self._popup.calendarWidget.setMaximumDate(max_date)
        self._popup.timeWidget.clearMaximumTime()

    def clearMaximumTime(self):
        self._datetime_edit.clearMaximumTime()
        self._popup.timeWidget.clearMaximumTime()

    def clearMinimumDate(self):
        self._datetime_edit.clearMinimumDate()
        min_date = self._datetime_edit.minimumDate()
        self._popup.calendarWidget.setMinimumDate(min_date)

    def clearMinimumDateTime(self):
        self._datetime_edit.clearMinimumDateTime()
        min_date = self._datetime_edit.maximumDate()
        self._popup.calendarWidget.setMinimumDate(min_date)
        self._popup.timeWidget.clearMinimumTime()

    def clearMinimumTime(self):
        self._datetime_edit.clearMinimumTime()
        self._popup.timeWidget.clearMinimumTime()

    def currentSection(self):
        raise NotImplementedError("Not implemented yet")

    def currentSectionIndex(self):
        raise NotImplementedError("Not implemented yet")

    def date(self):
        if not self._datetime_text:
            return None
        else:
            return self._datetime_edit.date()

    def dateTime(self):
        if not self._datetime_text:
            return None
        else:
            return self._datetime_edit.dateTime()

    def displayFormat(self):
        return self._popup.custom_datetime_settings.format

    def dateTimeFromText(self, text: str):
        if not isinstance(text, str):
            text_type = str(type(text)).split("'")[1]
            raise TypeError(
                f"""'DateTimeEdit.dateTimeFromText' called with wrong argument types:\n\t
                DateTimeEdit.dateTimeFromText({text_type})\n\t\t
                Supported signatures:\n\t
                DateTimeEdit.dateTimeFromText(str)"""
            )
        return self._datetime_edit.dateTimeFromText(text)

    def displayedSections(self):
        raise NotImplementedError("Not implemented yet")

    def maximumDate(self):
        return self._popup.calendarWidget.maximumDate()

    def maximumDateTime(self):
        return self._datetime_edit.maximumDateTime()

    def maximumTime(self):
        return self._popup.timeWidget.maximumTime()

    def minimumDate(self):
        return self._popup.calendarWidget.minimumDate()

    def minimumDateTime(self):
        return self._datetime_edit.minimumDateTime()

    def minimumTime(self):
        return self._popup.timeWidget.minimumTime()

    def mode(self):
        return self._mode

    def sectionAt(self, index):
        raise NotImplementedError("Not implemented yet")

    def sectionCount(self):
        raise NotImplementedError("Not implemented yet")

    def sectionText(self, section):
        raise NotImplementedError("Not implemented yet")

    def setCalendar(self, calendar):
        raise NotImplementedError("Not implemented yet")

    def setCalendarPopup(self, enable: bool):
        self._show_popup = enable
        if self._show_popup:
            self._popup_btn.setEnabled(True)
            self._popup.init_ui()
            self._popup_btn.clicked.connect(self._openCalendar)
        else:
            self._popup_btn.setEnabled(False)

    def setCalendarWidget(self, calendarWidget):
        self._datetime_edit.setCalendarWidget(calendarWidget)
        self._popup.calendarWidget = calendarWidget

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
        self._datetime_edit.setDate(date)
        self._popup.calendarWidget.setSelectedDate(date)
        self.setText(date.toString(self._popup.custom_datetime_settings.format))

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
        self._datetime_edit.setDateTime(dt)
        self._popup.calendarWidget.setSelectedDate(dt.date())
        self._popup.timeWidget.setTime(dt.time())
        self.setText(dt.toString(self._popup.custom_datetime_settings.format))

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
        self._datetime_edit.setDisplayFormat(format)
        self._popup.custom_datetime_settings.format = format

    def setMaximumDate(self, max):
        self._datetime_edit.setMaximumDate(max)
        self._popup.calendarWidget.setMaximumDate(max)

    def setMaximumDateTime(self, dt):
        self._datetime_edit.setMaximumDateTime(dt)
        self._popup.calendarWidget.setMaximumDate(dt.date())
        self._popup.timeWidget.setMaximumTime(dt.time())

    def setMaximumTime(self, max):
        self._datetime_edit.setMaximumTime(max)
        self._popup.timeWidget.setMaximumTime(max)

    def setMinimumDate(self, min):
        self._datetime_edit.setMinimumDate(min)
        self._popup.calendarWidget.setMinimumDate(min)

    def setMinimumDateTime(self, dt):
        self._datetime_edit.setMinimumDateTime(dt)
        self._popup.calendarWidget.setMinimumDate(dt.date())
        self._popup.timeWidget.setMinimumTime(dt.time())

    def setMinimumTime(self, min):
        self._datetime_edit.setMinimumTime(min)
        self._popup.timeWidget.setMinimumTime(min)

    def setMode(self, mode: Mode):
        if not isinstance(mode, Mode):
            mode_type = str(type(mode)).split("'")[1]
            raise TypeError(
                f"""'DateTimeEdit.setMode' called with wrong argument types:\n\t
                DateTimeEdit.setMode({mode_type})\n\t\t
                Supported signatures:\n\t
                DateTimeEdit.setMode(Mode)"""
            )
        self._mode = mode
        self._popup = DateTimePopup(self._mode, self)

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
        self._datetime_edit.setTime(time)
        self._popup.timeWidget.setTime(time)
        self.setText(time.toString(self._popup.custom_datetime_settings.format))

    def setTimeRange(self, min, max):
        self.setMinimumTime(min)
        self.setMaximumTime(max)

    def setTimeSpec(self, spec):
        self._datetime_edit.setTimeSpec(spec)

    def textFromDateTime(self, dt):
        self._datetime_edit.textFromDateTime(dt)

    def time(self):
        if not self._datetime_text:
            return None
        else:
            return self._datetime_edit.time()

    def timeSpec(self):
        return self._datetime_edit.timeSpec()
