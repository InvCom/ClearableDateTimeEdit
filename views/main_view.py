from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import Slot
from views.main_view_ui import Ui_MainWindow


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._ui.date_time_edit.timeWidget().showMsec(False)
        self._ui.date_time_edit_ps.dateTimeChanged.connect(self.set_text)
        self._ui.date_time_edit_ps.dateTimeChanged.connect(self._ui.date_time_edit.setDateTime)
        self._ui.date_time_edit_ps.dateChanged.connect(self.set_text)
        self._ui.date_time_edit_ps.timeChanged.connect(self.set_text)
        self._ui.date_time_edit.dateTimeChanged.connect(self.set_text)
        self._ui.date_time_edit.editingFinished.connect(self.set_text)
        self._ui.date_time_edit.dateChanged.connect(self.set_text)
        self._ui.date_time_edit.timeChanged.connect(self.set_text)
        self._ui.date_edit.dateTimeChanged.connect(self.set_text)
        self._ui.date_edit.editingFinished.connect(self.set_text)
        self._ui.time_edit.dateTimeChanged.connect(self.set_text)
        self._ui.time_edit.editingFinished.connect(self.set_text)
        self._ui.date_time_edit_wp.dateTimeChanged.connect(self.set_text)
        self._ui.date_time_edit_wp.editingFinished.connect(self.set_text)
        self._ui.pushButton_reset.clicked.connect(self.reset_text)

    def set_text(self, value):
        print(value)
        self._ui.label_even_odd.setText(value.toString() if value else "")

    def reset_text(self):
        self._ui.label_even_odd.clear()
