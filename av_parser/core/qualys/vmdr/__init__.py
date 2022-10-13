#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    __init__.py.py
# @Author:      d3x3r
# @Time:        10/10/22 18:42

from ._output import excel
from ._parser import parser

__all__ = [
    "parser",
    "excel",
]
