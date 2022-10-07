#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _output.py
# @Author:      Daniel Puente Ramírez
# @Time:        5/10/22 14:45

import pandas as pd

import variables as v
from av_parser.core.kiuwan.common import excel_col_format, \
    audit_company_and_width


def excel(df, path, sheet_name='Vulnerabilidades del código'):
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name, index=False, header=False,
                startrow=v.offset)

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    cell_format = workbook.add_format()
    cell_format.set_align('center')
    cell_format.set_align('vcenter')

    worksheet.set_column('A:O', None, cell_format)

    excel_col_format(df, workbook, worksheet, '#DD7E6B', 'Muy Alta', 'C')
    excel_col_format(df, workbook, worksheet, '#EA9999', 'Alta', 'C')
    excel_col_format(df, workbook, worksheet, '#F9CB9C', 'Normal', 'C')
    excel_col_format(df, workbook, worksheet, '#FFE599', 'Baja', 'C')
    excel_col_format(df, workbook, worksheet, '#B6D7A8', 'Muy Baja', 'C')

    v_center = workbook.add_format({'align': 'vcenter'})
    worksheet.conditional_format('A1:G{}'.format(len(df)),
                                 {
                                     'type': 'no_blanks',
                                     'format': v_center
                                 })

    soft_characteristics = workbook.add_format({'bold': True})
    worksheet.conditional_format('D{}:D{}'.format(v.offset, len(df) + v.offset),
                                 {
                                     'type': 'formula',
                                     'criteria': '=$D{}="{}"'.format(
                                         v.offset, 'Seguridad'),
                                     'format': soft_characteristics
                                 })

    audit_company_and_width(df, sheet_name, workbook, worksheet, writer,
                            v.kiuwan.vuln_excel_columns)

    worksheet.freeze_panes(v.offset, 4)

    writer.close()
    v.log.info('Excel file created: {}'.format(path))
