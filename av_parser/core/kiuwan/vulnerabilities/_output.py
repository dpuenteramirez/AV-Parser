#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _output.py
# @Author:      d3x3r
# @Time:        5/10/22 14:45

import os

import pandas as pd

import variables as v
from av_parser.core.common import audit_company_and_width
from av_parser.core.kiuwan.common import excel_col_format


def excel(df, path, sheet_name="Vulnerabilidades del código"):
    """It creates an Excel file
    with the vulnerabilities dataframe

    Parameters
    ----------
    df
        The dataframe to be written to the Excel file.
    path
        The path to the Excel file.
    sheet_name, optional
        The name of the sheet which will contain the data.

    """
    path = path.replace(".xlsx", "_vulns.xlsx")
    writer = pd.ExcelWriter(path, engine="xlsxwriter")
    df.to_excel(
        writer, sheet_name=sheet_name, index=False, header=False, startrow=v.offset
    )

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    cell_format = workbook.add_format()
    cell_format.set_align("center")
    cell_format.set_align("vcenter")

    worksheet.set_column("A:O", None, cell_format)

    excel_col_format(df, workbook, worksheet, "#DD7E6B", "Muy Alta", "C")
    excel_col_format(df, workbook, worksheet, "#EA9999", "Alta", "C")
    excel_col_format(df, workbook, worksheet, "#F9CB9C", "Normal", "C")
    excel_col_format(df, workbook, worksheet, "#FFE599", "Baja", "C")
    excel_col_format(df, workbook, worksheet, "#B6D7A8", "Muy Baja", "C")

    v_center = workbook.add_format({"align": "vcenter"})
    worksheet.conditional_format(
        f"A1:G{len(df)}", {"type": "no_blanks", "format": v_center}
    )

    soft_characteristics = workbook.add_format({"bold": True})
    worksheet.conditional_format(
        f"D{v.offset}:D{len(df) + v.offset}",
        {
            "type": "formula",
            "criteria": f'=$D{v.offset}="Seguridad"',
            "format": soft_characteristics,
        },
    )

    audit_company_and_width(
        df, sheet_name, workbook, worksheet, writer, v.kiuwan.vuln_excel_columns
    )

    worksheet.freeze_panes(v.offset, 4)

    writer.close()
    v.log.success(f"Excel file created: {path}")

    path = path.replace(".xlsx", "_vuln_charts.xlsx")
    writer = pd.ExcelWriter(path, engine="xlsxwriter")
    n_vulns = _excel_bar_chart_vulns(writer, path)
    _pie_chart_languages(n_vulns, writer)
    writer.close()


def _excel_bar_chart_vulns(writer, path, sheet_name="Charts"):
    """It creates a bar chart with the number of vulnerabilities per type

    Parameters
    ----------
    path
        The path to the Excel file.
    sheet_name, optional
        The name of the sheet to be created in the Excel file.

    Returns
    -------
        A function that takes two arguments, path and sheet_name.

    """
    try:
        df = pd.read_csv(os.path.join(v.temp_dir, "vuln_type.csv"))
    except pd.erros.EmptyDataError:
        v.log.warning("No vulnerabilities found")
        return

    except FileNotFoundError:
        v.log.warning(
            "Could not find a tmp file. Is it running with enough permissions?"
        )
        return

    df.to_excel(writer, sheet_name=sheet_name, index=False)

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    chart = workbook.add_chart({"type": "bar"})

    chart.add_series(
        {
            "name": "Vulnerabilities",
            "categories": f"='{sheet_name}'!$A$2:$A${len(df) + 1}",
            "values": f"='{sheet_name}'!$B$2:$B${len(df) + 1}",
            "data_labels": {"value": True},
            "fill": {"color": "#008000"},
        }
    )

    chart.set_title({"name": "Vulnerabilidades por tipo"})
    chart.set_legend({"none": True})
    chart.set_style(15)

    worksheet.insert_chart("E1", chart)

    v.log.success(f"Excel bar chart file created: {path}")

    return len(df) + 15


def _pie_chart_languages(offset, writer, sheet_name="Charts"):
    """It creates a pie chart with the languages used in the project

    Parameters
    ----------
    offset
        The row number where the chart will be inserted.
    writer
        the ExcelWriter object
    sheet_name, optional
        The name of the sheet to which the chart will be added.

    Returns
    -------
        A pie chart with the languages and the LOC of each one.

    """
    if len(v.kiuwan.languages) == 0:
        return

    df = pd.read_csv(os.path.join(v.temp_dir, "languages.csv"))
    df.columns = ["Language", "LOC"]

    percent_col = [
        f'A{i}&" - "&TEXT(C{i}/SUM($C${offset+1}:$C${len(df) + offset}),"0,' \
        f'00%")'
        for i in range(offset + 1, len(df) + offset + 1)
    ]

    df_langs = df["Language"].copy()
    df_loc = df["LOC"].copy()

    df_langs.to_excel(writer, sheet_name=sheet_name, index=False, header=False,
                      startrow=offset, startcol=0)

    df_loc.to_excel(writer, sheet_name=sheet_name, index=False, header=True,
                    startrow=offset-1, startcol=2)

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    for index, val in enumerate(percent_col):
        worksheet.write_formula(f'B{index + offset + 1}', val)

    chart = workbook.add_chart({"type": "doughnut"})
    chart.add_series(
        {
            "name": "Languages",
            "categories": f"='{sheet_name}'!$B${offset + 1}:$B${len(df) + offset}",
            "values": f"='{sheet_name}'!$C${offset + 1}:$C${len(df) + offset}",
        }
    )

    chart.set_title({"name": "Lenguajes"})
    chart.set_style(10)
    chart.set_legend({"percent": True, "position": "bottom"})

    worksheet.insert_chart(f"E{offset}", chart)
