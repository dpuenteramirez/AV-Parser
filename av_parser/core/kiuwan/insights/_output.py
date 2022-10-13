#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _output.py
# @Author:      d3x3r
# @Time:        6/10/22 11:20
import os

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
    df.to_excel(
        writer, sheet_name=sheet_name, index=False, header=False, startrow=v.offset
    )

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

    audit_company_and_width(
        df, sheet_name, workbook, worksheet, writer, v.kiuwan.insights_excel_columns
    )

    worksheet.freeze_panes(v.offset, 3)

    writer.close()

    path = path.replace(".xlsx", "_insights_charts.xlsx")
    writer = pd.ExcelWriter(path, engine="xlsxwriter")
    _chart_doughnut_components(writer, sheet_name)

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


def _chart_doughnut_components(writer, sheet_name="Charts"):
    df = pd.read_csv(os.path.join(v.temp_dir, "security_risk.csv"))
    df = pd.DataFrame(
        df["Security risk"].value_counts(dropna=True),
        index=v.kiuwan.insights_risk_types,
    )
    df_index = pd.DataFrame(df.index)
    percent_col = [
        f'A{i}&" - "&TEXT(C{i}/SUM($C$2:$C${len(df)+1}),"0,00%")'
        for i in range(2, len(df) + 2)
    ]

    df.fillna(0, inplace=True)
    df.to_excel(writer, sheet_name=sheet_name, startcol=2, index=False)
    df_index.to_excel(
        writer, sheet_name=sheet_name, startrow=1, startcol=0, index=False, header=False
    )

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    for index, val in enumerate(percent_col):
        worksheet.write_formula(f"B{index+2}", val)

    chart = workbook.add_chart({"type": "doughnut"})
    chart.add_series(
        {
            "name": "Componentes",
            "categories": f"={sheet_name}!$B$2:$B${len(df) + 1}",
            "values": f"={sheet_name}!$C$2:$C${len(df) + 1}",
            "points": [
                {"fill": {"color": "#D01012"}},
                {"fill": {"color": "#F3B530"}},
                {"fill": {"color": "D4E658"}},
                {"fill": {"color": "D4E658"}},
            ],
        }
    )
    chart.set_title({"name": "Riesgo de seguridad en componentes"})
    chart.set_style(10)
    chart.set_legend({"percent": True, "position": "bottom"})

    worksheet.insert_chart("E1", chart)
