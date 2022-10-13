#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _output.py
# @Author:      d3x3r
# @Time:        10/10/22 18:42

import os
import string
from random import choice

import numpy as np
import pandas as pd

import variables as v
from av_parser.core.common import (
    add_table,
    adjust_column_width,
    audit_company_and_width,
)


def excel(path):
    """It creates an Excel file with 5 sheets, each one with a different report

    Parameters
    ----------
    path
        The path to the Excel file to be created.

    """
    p_excel = v.log.progress("Creating Qualys VMDR Excel file")
    p_excel.status("Initializing...")

    writer = pd.ExcelWriter(path, engine="xlsxwriter")

    p_excel.status("Creating AV Results sheet...")
    _av_results(writer, "Resultados_AV")

    p_excel.status("Creating ID Unique Vulns sheet...")
    _id_unique_vulns(writer, "ID_Vulnerabilidades_Únicas")

    p_excel.status("Creating Host Severity sheet...")
    _host_severity(writer, "Hosts_Severidad")

    p_excel.status("Creating Host Unique Vulns sheet...")
    _host_unique_vulns(writer, "Hosts_Vulnerabilidades_Únicas")

    p_excel.status("Creating Top 5 Vulns sheet...")
    _top_5_vulns(writer, "Top_5_Vulnerabilidades")

    writer.close()

    p_excel.success("All Excel sheets have been created successfully")
    v.log.success("Qualys VMDR Excel file created successfully")


def _av_results(writer, sheet_name):
    """It reads in the CSV file, filters the dataframe to only include the
    columns we want, and then writes the dataframe to the Excel file

    Parameters
    ----------
    writer
        the ExcelWriter object
    sheet_name
        The name of the sheet in the Excel file.

    """
    df = pd.read_csv(os.path.join(v.temp_dir, v.files[-1] + ".csv"), sep="\t")

    df = df[v.qualys.VMDR.av_results]

    df.to_excel(
        writer, sheet_name=sheet_name, header=False, index=False, startrow=v.offset
    )

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    cell_format = workbook.add_format()
    cell_format.set_align("left")
    cell_format.set_align("vcenter")

    worksheet.set_column("A:P", None, cell_format)

    worksheet.set_column("A:P", 50)

    audit_company_and_width(
        df,
        sheet_name,
        workbook,
        worksheet,
        writer,
        v.qualys.VMDR.av_results_excel_columns,
        False,
    )

    worksheet.freeze_panes(v.offset, 0)


def _id_unique_vulns(writer, sheet_name):
    """It takes the last file in the list of files, reads it as a csv, and
    then creates a dataframe with the unique values of the "Title" column and
    their respective counts

    Parameters
    ----------
    writer
        the ExcelWriter object
    sheet_name
        The name of the sheet in the Excel file.

    """
    df = pd.read_csv(os.path.join(v.temp_dir, v.files[-1] + ".csv"), sep="\t")

    unique_names_occurrences = df["Title"].value_counts(dropna=True)

    df = pd.DataFrame(unique_names_occurrences)
    df.reset_index(inplace=True)

    ids = [
        f"AV-{v.av_data.company[:3].upper()}-{v.av_data.year}-"
        f"{str(int(v.av_data.starting_id) + i).zfill(6)}"
        for i in range(len(df))
    ]

    df.insert(0, "ID", ids)

    df.to_excel(writer, sheet_name=sheet_name, index=False, header=False, startrow=1)

    worksheet = writer.sheets[sheet_name]

    add_table(df, v.qualys.VMDR.id_unique_vulns_excel_columns, worksheet, 1)
    df.columns = [
        "".join(choice(string.ascii_lowercase) for _ in range(5))
        for _ in range(len(df.columns))
    ]
    adjust_column_width(df, sheet_name, writer)


def _host_severity(writer, sheet_name):
    """It takes the data from the last file in the list of files, groups it by
    IP and Severity, and then creates a table with the number of
    vulnerabilities per severity per IP

    Parameters
    ----------
    writer
        The ExcelWriter object
    sheet_name
        The name of the sheet in the Excel file.

    """
    df = pd.read_csv(os.path.join(v.temp_dir, v.files[-1] + ".csv"), sep="\t")
    df = df[v.qualys.VMDR.host_severity_columns]

    df = df.groupby(["IP", "Severity"]).size().reset_index(name="Count")

    df_host_vulns = pd.DataFrame(
        index=df["IP"].unique(), columns=v.qualys.VMDR.host_severity_excel_columns[1:]
    )

    df_host_vulns.fillna(0, inplace=True)

    for _, row in df.iterrows():
        df_host_vulns.loc[row["IP"], row["Severity"]] = row["Count"]

    total_vulns = df_host_vulns.sum(axis=1)
    df_host_vulns.insert(0, "Total", total_vulns)
    df_host_vulns.sort_values(by="Total", ascending=False, inplace=True)
    df_host_vulns.drop("Total", axis=1, inplace=True)

    df_host_vulns.reset_index(inplace=True)
    df_host_vulns.columns = v.qualys.VMDR.host_severity_excel_columns

    df_host_vulns.to_excel(
        writer, sheet_name=sheet_name, index=False, header=False, startrow=1
    )

    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    add_table(
        df_host_vulns,
        v.qualys.VMDR.host_severity_excel_columns,
        worksheet,
        1,
        "Table_VulnsHost",
        True,
        f"=SUM(Table_VulnsHost[[#This Row],["
        f"{v.qualys.VMDR.host_severity_excel_columns[1]}]:["
        f"{v.qualys.VMDR.host_severity_excel_columns[-1]}]])",
    )

    __distribution_vulns(df_host_vulns, workbook, worksheet)
    __vuln_distribution_chart(workbook, worksheet, sheet_name)

    for severity in v.qualys.VMDR.host_severity_excel_columns[1:]:
        __top_10_host_severity_chart(workbook, worksheet, sheet_name, severity)

    __top_10_host_more_vulns_chart(workbook, worksheet, sheet_name)
    worksheet.set_column("A:A", 20)


def _host_unique_vulns(writer, sheet_name):
    """It takes the last file in the list of files, reads it as a csv, and
    then creates a dataframe with the unique IPs. It then writes that
    dataframe to an Excel sheet, and then adds a table to the sheet

    Parameters
    ----------
    writer
        the ExcelWriter object
    sheet_name
        The name of the Excel sheet.

    """
    buscar_v1 = (
        "IF(VLOOKUP(A{},Table_Resultados_AV[[Host]:[DNS]],2,"
        "FALSE)<>0,VLOOKUP(A{},Table_Resultados_AV[[Host]:[DNS]],2,"
        'FALSE),"Not found")'
    )
    buscar_v2 = "VLOOKUP(A{},Table_VulnsHost[[Host]:[Critical]],6,FALSE)"

    df = pd.read_csv(os.path.join(v.temp_dir, v.files[-1] + ".csv"), sep="\t")

    df = pd.DataFrame(df["IP"].unique())

    df.to_excel(writer, sheet_name=sheet_name, index=False, header=False, startrow=1)

    worksheet = writer.sheets[sheet_name]

    for n_row in range(2, len(df) + 2):
        worksheet.write_formula(f"B{n_row}", buscar_v1.format(n_row, n_row))
        worksheet.write_formula(f"C{n_row}", buscar_v2.format(n_row))

    add_table(df, v.qualys.VMDR.host_unique_vulns_excel_columns, worksheet, 1)
    df.columns = [
        "".join(choice(string.ascii_lowercase) for _ in range(5))
        for _ in range(len(df.columns))
    ]
    adjust_column_width(df, sheet_name, writer)
    worksheet.set_column("B:B", 50)


def _top_5_vulns(writer, sheet_name):
    """It takes the last file in the list of files, reads it into a dataframe,
    filters the dataframe to only include the columns we want, groups the
    dataframe by the title and severity of the vulnerability, sums the number of
    vulnerabilities for each title and severity, sorts the dataframe by the
    number of vulnerabilities, and writes the dataframe to an Excel file

    Parameters
    ----------
    writer
        the ExcelWriter object
    sheet_name
        The name of the sheet in the Excel file.

    """
    df = pd.read_csv(os.path.join(v.temp_dir, v.files[-1] + ".csv"), sep="\t")

    df = df[v.qualys.VMDR.top_5_vulns_columns]

    df = df.groupby(["Title", "Severity"]).size().reset_index(name="Count")

    for severity in v.qualys.VMDR.map_severity.values():
        n_severity = df[df["Severity"] == severity]["Count"].sum()
        if n_severity > 0:
            df = df[df["Severity"] == severity]
            df.drop("Severity", axis=1, inplace=True)
            v.qualys.VMDR.top_5_vulns_excel_columns[
                1
            ] = v.qualys.VMDR.top_5_vulns_excel_columns[1].format(severity)
            break

    df.sort_values(by="Count", ascending=False, inplace=True)

    df.to_excel(writer, sheet_name=sheet_name, index=False, header=False, startrow=1)

    worksheet = writer.sheets[sheet_name]

    add_table(df, v.qualys.VMDR.top_5_vulns_excel_columns, worksheet, 1)
    adjust_column_width(df, sheet_name, writer)
    worksheet.set_column("B:B", len(v.qualys.VMDR.top_5_vulns_excel_columns[1]))


def __distribution_vulns(df, workbook, worksheet):
    """It takes a dataframe, a workbook, and a worksheet, and writes the total
    number of vulnerabilities for each severity level to the worksheet

    Parameters
    ----------
    df
        The dataframe that contains the data to be written to the Excel file.
    workbook
        The workbook object that we created earlier.
    worksheet
        The worksheet object that you want to write to.

    """
    sums = df.select_dtypes(np.number).sum().rename("Total")

    cell_format_header = workbook.add_format(
        {
            "align": "center",
            "valign": "vcenter",
            "font_color": "#008000",
        }
    )

    cell_format_bold = workbook.add_format()
    cell_format_bold.set_bold()

    worksheet.write("J1", "Info", cell_format_header)
    worksheet.write("K1", "Low", cell_format_header)
    worksheet.write("L1", "Medium", cell_format_header)
    worksheet.write("M1", "High", cell_format_header)
    worksheet.write("N1", "Critical", cell_format_header)
    worksheet.write("O1", "Total", cell_format_header)
    worksheet.write("I2", "Total", cell_format_bold)
    worksheet.write("J2", sums["Info"])
    worksheet.write("K2", sums["Low"])
    worksheet.write("L2", sums["Medium"])
    worksheet.write("M2", sums["High"])
    worksheet.write("N2", sums["Critical"])
    worksheet.write_formula("O2", "=SUM(J2:N2)", cell_format_bold)


def __vuln_distribution_chart(workbook, worksheet, sheet_name):
    """It creates a bar chart with the number of vulnerabilities per severity
    level

    Parameters
    ----------
    workbook
        The workbook object.
    worksheet
        The worksheet object.
    sheet_name
        The name of the sheet that contains the data for the chart.

    """
    chart = workbook.add_chart({"type": "bar"})
    chart.add_series(
        {
            "name": "VulnerabilitiesDistribution",
            "categories": f"={sheet_name}!$J$1:$N$1",
            "values": f"={sheet_name}!$J$2:$N$2",
            "data_labels": {"value": True},
            "fill": {"color": "#008000"},
        }
    )

    chart.set_x_axis(
        {
            "line": {"color": "#E0DCDC"},
            "major_gridlines": {"visible": False},
            "values": v.qualys.VMDR.host_severity_excel_columns[1:],
        }
    )
    chart.set_y_axis(
        {
            "line": {"none": True},
            "major_gridlines": {
                "visible": True,
                "line": {"width": 1, "color": "#E0DCDC"},
            },
        }
    )

    chart.set_title({"name": "Distribución de vulnerabilidades detectadas"})
    chart.set_legend({"none": True})
    chart.set_style(15)
    worksheet.insert_chart(
        "P1", chart, {"x_offset": 25, "y_offset": 10, "x_scale": 1, "y_scale": 1}
    )


def __top_10_host_severity_chart(workbook, worksheet, sheet_name, severity):
    """It creates a chart with the top 10 hosts with the most vulnerabilities
    of a given severity

    Parameters
    ----------
    workbook
        The workbook object.
    worksheet
        The worksheet object.
    sheet_name
        The name of the sheet that the chart will be placed on.
    severity
        The severity of the vulnerabilities to be displayed in the chart.

    """
    n_severity = v.qualys.VMDR.host_severity_excel_columns.index(severity)
    letter = string.ascii_uppercase[n_severity]

    chart = workbook.add_chart({"type": "column"})
    chart.add_series(
        {
            "name": f"Top10Host{severity}Severity",
            "categories": f"={sheet_name}!$A$2:$A$12",
            "values": f"={sheet_name}!${letter}$2:${letter}$12",
            "data_labels": {"value": True},
            "fill": {"color": "#008000"},
        }
    )

    chart.set_x_axis(
        {
            "line": {"color": "#E0DCDC"},
            "major_gridlines": {"visible": False},
        }
    )
    chart.set_y_axis(
        {
            "line": {"none": True},
            "major_gridlines": {
                "visible": True,
                "line": {"width": 1, "color": "#E0DCDC"},
            },
        }
    )

    chart.set_title(
        {
            "name": f"Hosts con mayor cantidad de "
            f"vulnerabilidades de tipo '{severity}'"
        }
    )
    chart.set_legend({"none": True})
    chart.set_style(15)

    y_offset = n_severity * 300

    worksheet.insert_chart(
        f"P{n_severity}",
        chart,
        {"x_offset": 25, "y_offset": y_offset, "x_scale": 1, "y_scale": 1},
    )


def __top_10_host_more_vulns_chart(workbook, worksheet, sheet_name):
    """It creates a chart with the top 10 hosts with more vulnerabilities

    Parameters
    ----------
    workbook
        The workbook object.
    worksheet
        The worksheet object.
    sheet_name
        The name of the sheet that contains the data.

    """
    chart = workbook.add_chart({"type": "column", "subtype": "stacked"})

    for severity in v.qualys.VMDR.host_severity_excel_columns[1:]:
        n_severity = v.qualys.VMDR.host_severity_excel_columns.index(severity)
        letter = string.ascii_uppercase[n_severity]
        chart.add_series(
            {
                "name": severity,
                "categories": f"={sheet_name}!$A$2:$A$12",
                "values": f"={sheet_name}!${letter}$2:${letter}$12",
            }
        )

    line_chart = workbook.add_chart({"type": "line"})

    line_chart.add_series(
        {
            "name": "Total",
            "categories": f"={sheet_name}!$A$2:$A$12",
            "values": f"={sheet_name}!$G$2:$G$12",
            "data_labels": {
                "value": True,
                "border": {"color": "red"},
                "fill": {"color": "yellow"},
                "position": "top",
            },
            "line": {"none": True, "color": "yellow"},
        }
    )

    chart.combine(line_chart)

    chart.set_x_axis(
        {
            "line": {"color": "#E0DCDC"},
            "major_gridlines": {"visible": False},
        }
    )

    chart.set_y_axis(
        {
            "line": {"none": True},
            "major_gridlines": {
                "visible": True,
                "line": {"width": 1, "color": "#E0DCDC"},
            },
        }
    )

    chart.set_title({"name": "Hosts con mayor cantidad de vulnerabilidades"})
    chart.set_legend(
        {
            "position": "bottom",
            "delete_series": [5],
        }
    )

    chart.set_style(18)

    worksheet.insert_chart(
        "I4", chart, {"x_offset": -25, "y_offset": 10, "x_scale": 1, "y_scale": 2}
    )
