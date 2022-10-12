#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _output.py
# @Author:      d3x3r
# @Time:        6/10/22 11:20

import pandas as pd

import variables as v
from av_parser.core.common import audit_company_and_width
from av_parser.core.kiuwan.common import excel_col_format


def excel_components(df, path, sheet_name="Componentes"):
    """It takes a dataframe,
    writes it to an Excel file, and formats the Excel file

    Parameters
    ----------
    df
        The dataframe to be written to excel_components
    path
        the path to the Excel file
    sheet_name, optional
        The name of the sheet to be created in the Excel file.

    """
    path = path.replace(".xlsx", "_components.xlsx")

    writer = pd.ExcelWriter(path, engine="xlsxwriter")
    df.to_excel(writer,
                sheet_name=sheet_name,
                index=False,
                header=False,
                startrow=v.offset)

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    cell_format_center = workbook.add_format()
    cell_format_center.set_align("center")
    cell_format_center.set_align("vcenter")

    cell_format_left = workbook.add_format()
    cell_format_left.set_align("left")
    cell_format_left.set_align("vcenter")

    worksheet.set_column("B:D", None, cell_format_center)
    worksheet.set_column("A:A", None, cell_format_left)
    worksheet.set_column("E:L", None, cell_format_left)

    text_colors = {
        "Alto": "#DD7E6B",
        "Medio": "#F9CB9C",
        "Bajo": "#FFE598",
        "Ninguno": "#B7D7A8",
        "Desconocido": "#FFFFFF",
    }

    for letter in ["B", "C", "D"]:
        for text, color in text_colors.items():
            excel_col_format(df, workbook, worksheet, color, text, letter)

    audit_company_and_width(df, sheet_name, workbook, worksheet, writer,
                            v.kiuwan.insights_excel_columns)

    worksheet.freeze_panes(v.offset, 3)

    writer.close()


def cli_license(df):
    """It prints the number of high and medium risk licenses in the dataframe

    Parameters
    ----------
    df
        The dataframe that contains the data.

    Returns
    -------
        The number of vulnerabilities with a high or medium risk.

    """
    try:
        values = df["Risk"].value_counts(dropna=True)
    except KeyError:
        return
    print("\n\n------------------ Licencias ------------------\n")
    if "High" in values:
        print(f'High: {values["high"]}')
    if "Medium" in values:
        print(f'Medium: {values["medium"]}')


def cli_output(df, values, title):
    """It takes a dataframe, a list of values, and a title, and prints out the
    number of times each value appears in the dataframe.

    Parameters
    ----------
    df
        The dataframe to be analyzed
    values
        The values you want to count.
    title
        The title of the dataframe

    Returns
    -------
        The number of times each risk value appears in the dataframe.

    """
    try:
        risk_values = df["Risk"].value_counts(dropna=True)
    except KeyError:
        return

    print(f"\n\n------------------ {title} ------------------\n")

    for value in values:
        if value in risk_values:
            print(f"{value}: {risk_values[value]}")
