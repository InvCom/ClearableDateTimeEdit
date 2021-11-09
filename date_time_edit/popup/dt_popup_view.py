# -*- coding: utf-8 -*-
from PySide2.QtCore import QObject, QDate
from PySide2.QtWidgets import QWidget, QListWidgetItem, QCalendarWidget

from date_time_edit.popup.classes import CustomTimeHelper, CustomDateTimeHelper, CustomDateHelper
from date_time_edit.popup.dt_popup_ui import DateTimePopupUi
from date_time_edit.settings import Mode


# self.start_search_date.setDisplayFormat("dd.MM.yyyy")
# self.start_search_date.calendarWidget().setLocale(
#     QLocale(QLocale.German, QLocale.Germany)
# )

class DateTimePopup(QWidget):
    def __init__(self, mode, parent):
        super(DateTimePopup, self).__init__(parent)
        self.ui = DateTimePopupUi()
        self.ui.setupUi(self)
        self._mode = mode
        self._custom_datetime_settings = self._get_datetime_class()

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
    def custom_datetime_settings(self) -> QObject:
        """Gets settings for datetime, date or time popup.

        Returns:
             QObject: Settings for datetime, date or time popup.

        """
        return self._custom_datetime_settings

    def init_ui(self):
        self._custom_datetime_settings.init_ui()

    def _get_datetime_class(self):
        mode_class_map = {
            Mode.time.value: CustomTimeHelper,
            Mode.date.value: CustomDateHelper,
            Mode.datetime.value: CustomDateTimeHelper,
        }
        return mode_class_map.get(self._mode.value, CustomDateTimeHelper)(self)

    def reset(self):
        self.ui.calendarWidget.setSelectedDate(QDate.currentDate())
        self.ui.timeWidget.reset()

    def set_today(self):
        self.ui.calendarWidget.setSelectedDate(QDate.currentDate())
        self.ui.timeWidget.set_today()
