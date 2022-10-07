#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    __init__.py.py
# @Author:      Daniel Puente Ramírez
# @Time:        6/10/22 16:28

import variables as v


def mapping_df(df, parse_columns, columns_to_map, mapping_dict):
    df = df.filter(items=parse_columns, axis=1)

    ids = ['COD-{}-{}-{}'.format(
        v.av_data.company,
        v.av_data.year,
        str(int(v.av_data.starting_id) + i).zfill(6)) for i in range(len(df))]

    df.insert(0, 'ID', ids)

    for index, column in enumerate(columns_to_map):
        df[column] = df[column].map(mapping_dict[index])

    return df


def excel_col_format(df, workbook, worksheet, bg_color, criteria,
                     column_letter, bold=True):
    formatting = workbook.add_format({
        'bold': bold,
        'bg_color': bg_color,
    })
    worksheet.conditional_format('{}{}:{}{}'.format(
        column_letter, v.offset, column_letter,
        len(df) + v.offset), {
        'type': 'formula',
        'criteria': '=${}{}="{}"'.format(column_letter, v.offset, criteria),
        'format': formatting
    }
    )


def audit_company_and_width(df, sheet_name, workbook, worksheet, writer,
                            header):
    summary_info_format = workbook.add_format({'bold': True,
                                               'bg_color': '#79A353'})
    summary_values_format = workbook.add_format({'bg_color': '#ACF06E'})
    worksheet.write('A8', 'Empresa', summary_info_format)
    worksheet.write('A9', 'Componente', summary_info_format)
    worksheet.write('A10', 'Empresa auditora', summary_info_format)
    worksheet.write('A11', 'Fecha auditoría', summary_info_format)
    worksheet.write('A12', 'Versión', summary_info_format)
    worksheet.write('B8', v.av_data.company, summary_values_format)
    worksheet.write('B9', v.av_data.component, summary_values_format)
    worksheet.write('B10', v.av_data.auditor, summary_values_format)
    worksheet.write('B11', v.av_data.audit_date, summary_values_format)
    worksheet.write('B12', v.av_data.version, summary_values_format)
    headers = [{'header': col} for col in header]
    worksheet.add_table('A{}:O{}'.format(v.offset, len(df) + v.offset),
                        {'columns': headers,
                         'style': 'Table Style Medium 18'
                         })
    _adjust_column_width(df, sheet_name, writer)
    worksheet.insert_image('A1', 'resources/mnemo_logo.png',
                           {'x_scale': 0.5,
                            'y_scale': 0.5})


def _adjust_column_width(df, sheet_name, writer):
    for column in df:
        column_length = max(df[column].astype(str).map(len).max(),
                            len(column)) + 10
        col_idx = df.columns.get_loc(column)
        writer.sheets[sheet_name].set_column(col_idx, col_idx, column_length)

    return writer
