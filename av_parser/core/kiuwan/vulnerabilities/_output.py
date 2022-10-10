#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _output.py
# @Author:      d3x3r
# @Time:        5/10/22 14:45

import os

import pandas as pd

import variables as v
from av_parser.core.kiuwan.common import audit_company_and_width, \
    excel_col_format


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
    df.to_excel(writer,
                sheet_name=sheet_name,
                index=False,
                header=False,
                startrow=v.offset)

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
    worksheet.conditional_format("A1:G{}".format(len(df)), {
        "type": "no_blanks",
        "format": v_center
    })

    soft_characteristics = workbook.add_format({"bold": True})
    worksheet.conditional_format(
        "D{}:D{}".format(v.offset,
                         len(df) + v.offset),
        {
            "type": "formula",
            "criteria": '=$D{}="{}"'.format(v.offset, "Seguridad"),
            "format": soft_characteristics,
        },
    )

    audit_company_and_width(df, sheet_name, workbook, worksheet, writer,
                            v.kiuwan.vuln_excel_columns)

    worksheet.freeze_panes(v.offset, 4)

    writer.close()
    v.log.success(f"Excel file created: {path}")

    _excel_bar_chart(path)


def _excel_bar_chart(path, sheet_name="Vulnerabilities types"):
    path = path.replace(".xlsx", "_bar_chart.xlsx")
    writer = pd.ExcelWriter(path, engine="xlsxwriter")

    try:
        df = pd.read_csv(os.path.join(v.temp_dir, "vuln_type.csv"))
    except pd.erros.EmptyDataError:
        v.log.warning("No vulnerabilities found")
        return

    except FileNotFoundError:
        v.log.warning("Could not find a tmp file. Is it running with "
                      "enough permissions?")
        return

    df.to_excel(writer, sheet_name=sheet_name, index=False)

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    chart = workbook.add_chart({"type": "bar"})

    chart.add_series({
        "name": "Vulnerabilities",
        "categories": "='{}'!$A$2:$A${}".format(sheet_name, len(df) + 1),
        "values": "='{}'!$B$2:$B${}".format(sheet_name, len(df) + 1),
        "data_labels": {"value": True},
        "fill": {"color": "#008000"},
    })

    chart.set_title({"name": "Vulnerabilidades por tipo"})
    chart.set_legend({'none': True})
    chart.set_style(15)

    worksheet.insert_chart("A10", chart)

    writer.close()
    v.log.success(f"Excel bar chart file created: {path}")
