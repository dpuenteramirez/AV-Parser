#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _parser.py
# @Author:      d3x3r
# @Time:        5/10/22 11:35

import pandas as pd

import variables as v
from av_parser.core.kiuwan.common import mapping_df


def parser(path, sep=","):
    """It reads in a CSV file, maps the values of two columns to new values, and
    renames the columns

    Parameters
    ----------
    path
        the path to the CSV file
    sep, optional
        the separator used in the CSV file.

    Returns
    -------
        A dataframe with the columns renamed to match the vuln_excel_columns

    """
    df = pd.read_csv(path, sep=sep)

    df = mapping_df(
        df,
        v.kiuwan.vuln_parse_columns,
        ["Priority", "Software characteristic"],
        [v.kiuwan.priority_map, v.kiuwan.software_characteristic_map],
    )

    df.columns = v.kiuwan.vuln_excel_columns[:-1]

    return df
