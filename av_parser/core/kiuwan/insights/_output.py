#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _output.py
# @Author:      Daniel Puente Ramírez
# @Time:        6/10/22 11:20

import pandas as pd

import variables as v
from av_parser.core.kiuwan.common import excel_col_format, \
    audit_company_and_width


def excel(df, path, sheet_name='Componentes'):
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name, index=False, header=False,
                startrow=v.offset)

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    cell_format_center = workbook.add_format()
    cell_format_center.set_align('center')
    cell_format_center.set_align('vcenter')

    cell_format_left = workbook.add_format()
    cell_format_left.set_align('left')
    cell_format_left.set_align('vcenter')

    worksheet.set_column('B:D', None, cell_format_center)
    worksheet.set_column('A:A', None, cell_format_left)
    worksheet.set_column('E:L', None, cell_format_left)

    text_colors = {
        'Alto': '#DD7E6B',
        'Medio': '#F9CB9C',
        'Bajo': '#FFE598',
        'Ninguno': '#B7D7A8',
        'Desconocido': '#FFFFFF'
    }

    for letter in ['B', 'C', 'D']:
        for text, color in text_colors.items():
            excel_col_format(df, workbook, worksheet, color, text, letter)

    audit_company_and_width(df, sheet_name, workbook, worksheet, writer,
                            v.kiuwan.insights_excel_columns)

    worksheet.freeze_panes(v.offset, 3)

    writer.close()
