# -*- coding: utf-8 -*-
__all__ = ["Mode"]
from enum import Enum


class Mode(Enum):
    date = "date"
    datetime = "datetime"
    time = "time"
