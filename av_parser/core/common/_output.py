#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _output.py
# @Author:      d3x3r
# @Time:        11/10/22 08:30

import string

import variables as v


def audit_company_and_width(
    df, sheet_name, workbook, worksheet, writer, header=None, width=True
):
    """It writes the summary information of the audit, adds a table with the
     headers, and adjusts the column width

    Parameters
    ----------
    df
        The dataframe to calculate widths.
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
    width, optional
        If True, it will adjust the column width.

    """
    summary_info_format = workbook.add_format({"bold": True, "bg_color": "#79A353"})
    summary_values_format = workbook.add_format({"bg_color": "#ACF06E"})
    worksheet.write("A8", "Empresa", summary_info_format)
    worksheet.write("A9", "Componente", summary_info_format)
    worksheet.write("A10", "Empresa auditora", summary_info_format)
    worksheet.write("A11", "Fecha auditoría", summary_info_format)
    worksheet.write("A12", "Versión", summary_info_format)
    worksheet.write("B8", v.av_data.company, summary_values_format)
    worksheet.write("B9", v.av_data.component, summary_values_format)
    worksheet.write("B10", v.av_data.auditor, summary_values_format)
    worksheet.write("B11", v.av_data.audit_date, summary_values_format)
    worksheet.write("B12", v.av_data.version, summary_values_format)

    if header is not None:
        add_table(df, header, worksheet)

    if width:
        adjust_column_width(df, sheet_name, writer)

    worksheet.insert_image(
        "A1", "resources/mnemo_logo.png", {"x_scale": 0.5, "y_scale": 0.5}
    )


def add_table(df, header, worksheet, offset=-1, name="", total_col=False, formula=""):
    """> This function adds a table to a worksheet with the given dataframe,
    header, and worksheet.

    Parameters
    ----------
    df
        The dataframe you want to add to the worksheet
    header
        The header of the table.
    worksheet
        The worksheet you want to add the table to
    offset
        The row number where the table will start.
    name
        The name of the table.
    total_col, optional
        If you want to add a total column to the table, set this to True.
    formula
        The formula to be used for the total column.

    """
    offset = v.offset if offset == -1 else offset
    headers = [{"header": col} for col in header]

    if total_col:
        headers.append({"header": "Total", "formula": formula})

    if name == "":
        name = f"Table_{worksheet.name}"
        name = name.replace(" ", "_")

    table_width_letter = string.ascii_uppercase[len(headers) - 1]
    worksheet.add_table(
        f"A{offset}:{table_width_letter}{offset + len(df.index)}",
        {"name": name, "columns": headers, "style": "Table Style Medium 18"},
    )


def adjust_column_width(df, sheet_name, writer):
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
        column_length = max(df[column].astype(str).map(len).max(), len(column)) + 10
        col_idx = df.columns.get_loc(column)
        writer.sheets[sheet_name].set_column(col_idx, col_idx, column_length)

    return writer
