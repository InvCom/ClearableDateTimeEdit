# -*- coding: utf-8 -*-
"""This module contains mode of DateTimeEdit widget."""
__all__ = ["Mode"]
from enum import Enum


class Mode(Enum):
    """Possible modes of DateTimeEdit widget."""

    date = "date"
    datetime = "datetime"
    time = "time"
