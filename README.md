# ClearableDateTimeEdit
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-yellow)](https://www.python.org)
[![PySide2](https://img.shields.io/static/v1?label=PySide2&message=5.15.2&color=green)](https://pypi.org/project/PySide2)

In this project, a custom DateTimeEdit widget based on PySide2's QDateTimeEdit and QEditLine is developed in Python. The
DateTimeEdit allows the previously selected date/time to be deleted, so that the UI element can be left empty compared 
to the QDateTimeEdit from PySide2. With the widget it is further possible to set the mode for selecting the date, time 
or datetime. The input of the time is possible via a TimeWidget and not limited to direct input via keyboard as in 
QDateTimeEdit from PySide2.

## Requirements
- Python >= 3.7
- PySide2 = 5.15.2

## Installation
To install the current version from GitHub

```shell script
git clone https://github.com/InvCom/ClearableDateTimeEdit.git
cd ClearableDateTimeEdit
pip3 install .
```

## How to Use
To be used, the ClearableDateTimeEdits widget is imported and initialised in the view file.
```python
from ClearableDateTimeEdit.Widgets import ClearableDateTimeEdit

self.date_time_edit = ClearableDateTimeEdit(self.centralwidget)
self.date_time_edit.setObjectName(u"ClearableDateTimeEdit")
self.layout.addWidget(self.date_time_edit)
```
ClearableDateTimeEdit starts in datetime mode by default. To change the mode, the preferred mode is passed during 
initialisation.
```python
from ClearableDateTimeEdit.Settings import Mode
from ClearableDateTimeEdit.Widgets import ClearableDateTimeEdit

self.date_time_edit = ClearableDateTimeEdit(self.centralwidget, Mode.date)
self.date_time_edit.setObjectName(u"ClearableDateTimeEdit")
self.layout.addWidget(self.date_time_edit)
```
Three modes are possible:
 - Mode.datetime<br>![datetime](https://user-images.githubusercontent.com/94013405/170215259-58930e55-2528-449f-900a-98efec622702.png)
 - Mode.date<br>![date](https://user-images.githubusercontent.com/94013405/170215342-a29914a5-8fd1-4718-a785-9c8f7daef683.png)
 - Mode.time<br>![time](https://user-images.githubusercontent.com/94013405/170215369-5688e830-3e88-4905-abd1-6e3c657cfcab.png)

The calendar and time widgets are displayed as a pop-up. The display can be deactivated and the input can be changed to 
keyboard input only.
```python
self.date_time_edit.setCalendarPopup(False)
```

With the ClearableDateTimeEdit it is possible to make most of the settings of the QDateTimeEdit from PySide2. Changing 
the display format, for example, is realised as in QDateTimeEdit.
```python
self.date_time_edit.setDisplayFormat("hh:mm:ss")
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
