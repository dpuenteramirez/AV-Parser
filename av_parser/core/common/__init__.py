#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    __init__.py.py
# @Author:      d3x3r
# @Time:        11/10/22 08:29

from ._output import add_table, adjust_column_width, audit_company_and_width

__all__ = [
    "audit_company_and_width",
    "adjust_column_width",
    "add_table",
]
