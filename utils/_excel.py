#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _excel.py
# @Author:      d3x3r
# @Time:        16/9/22 18:11

import openpyxl as xl
import variables as v


def control_excel_creation():
    """
    Control the creation of the Excel file.
    """
    _create_excel()


def _create_excel():
    """
    Create the Excel file.
    """
    wb = xl.Workbook()
    ws = wb.active
    ws.title = 'AV-Results'

    _av_results(wb)

    wb.save(v.output)
    v.log.success(v.str['file_created'].format(v.output))


def _av_results(wb):
    """
    Create the AV-Results sheet.

    #TODO
    """
