#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    __init__.py.py
# @Author:      d3x3r
# @Time:        10/10/22 16:55

import os

import pandas as pd

import variables as v
from av_parser.core.kiuwan.insights import (
    cli_output,
    excel_components,
    parser_components,
    parser_license,
    parser_obsolescence,
    parser_security,
)
from av_parser.core.kiuwan.vulnerabilities import excel as vuln_excel
from av_parser.core.kiuwan.vulnerabilities import parser as vuln_parser


def parser_full(dir_path, sep=","):
    v.log.info("Parsing Kiuwan all available data")
    files = os.listdir(dir_path)

    if len(files) == 0:
        v.log.failure("No files found in the directory")
        return

    for file in files:
        if file.endswith(".csv"):

            df = pd.read_csv(os.path.join(dir_path, file), sep=sep)

            if _check_lists(df.columns,
                            v.kiuwan.vulnerabilities_parse_columns):
                df = vuln_parser(os.path.join(dir_path, file))
                vuln_excel(df, v.output)
                v.log.success(f"File '{file}' recognized as vulns")

            if _check_lists(df.columns,
                            v.kiuwan.insights_components_parse_columns):
                df = parser_components(os.path.join(dir_path, file))
                excel_components(df, v.output)
                v.log.success(f"File '{file}' parsed as a componentes file")

            elif _check_lists(df.columns,
                              v.kiuwan.insights_license_parse_columns):
                df = parser_license(os.path.join(dir_path, file))
                cli_output(df, ["high", "medium"], "Licencias")
                v.log.success(f"File '{file}' parsed as a license file")

            elif _check_lists(df.columns,
                              v.kiuwan.insights_obsolescence_parse_columns):
                df = parser_obsolescence(os.path.join(dir_path, file))
                cli_output(df, ["High", "Medium"], "Obsolescencia")

                v.log.success(f"File '{file}' parsed as a obsolescence file")

            elif _check_lists(df.columns,
                              v.kiuwan.insights_security_parse_columns):
                df = parser_security(os.path.join(dir_path, file))
                cli_output(df, ["high", "medium"], "Seguridad")
                v.log.success(f"File '{file}' parsed as a security file")


def _check_lists(list1, list2):
    if len(list1) == len(list2) and len(list1) == sum(
            [1 for i, j in zip(list1, list2) if i == j]):
        return True
    else:
        return False
