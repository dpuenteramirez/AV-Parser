#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    __init__.py.py
# @Author:      d3x3r
# @Time:        6/10/22 16:28

import variables as v


def mapping_df(df, parse_columns, columns_to_map, mapping_dict):
    """It takes a dataframe, a list of columns to parse, a list of columns to
    map, and a list of dictionaries to map the columns to, and returns a
    dataframe with the columns mapped

    Parameters
    ----------
    df
        the dataframe to be mapped
    parse_columns
        the columns that you want to keep in the final dataframe
    columns_to_map
        a list of columns to map
    mapping_dict
        a list of dictionaries, each dictionary is a mapping for a column

    Returns
    -------
        A dataframe with the columns specified in parse_columns, with the
        columns specified in columns_to_map mapped to the values in the
        mapping_dict.

    """
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
    """This function takes a dataframe, workbook, worksheet, background color,
    criteria, and column letter as inputs and formats the column letter in the
    worksheet with the background color and bold formatting
    if the criteria is met

    Parameters
    ----------
    df
        the dataframe you're working with
    workbook
        the workbook object
    worksheet
        the worksheet you're working with
    bg_color
        the background color of the cell
    criteria
        the criteria to be met for the formatting to be applied
    column_letter
        The column letter of the column you want to format.
    bold, optional
        True/False

    """
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
    """It writes the summary information of the audit, adds a table with the
     headers, and adjusts the column width

    Parameters
    ----------
    df
        The dataframe to be written to Excel.
    sheet_name
        The name of the Excel sheet.
    workbook
        The workbook object.
    worksheet
        The worksheet object.
    writer
        the ExcelWriter object
    header
        list of column names

    """
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
    """For each column in the dataframe, find the length of the longest string
    in the column, and set the column width to that length plus 10

    Parameters
    ----------
    df
        The dataframe you want to export
    sheet_name
        The name of the Excel sheet.
    writer
        the ExcelWriter object

    Returns
    -------
        The writer object is being returned.

    """
    for column in df:
        column_length = max(df[column].astype(str).map(len).max(),
                            len(column)) + 10
        col_idx = df.columns.get_loc(column)
        writer.sheets[sheet_name].set_column(col_idx, col_idx, column_length)

    return writer
