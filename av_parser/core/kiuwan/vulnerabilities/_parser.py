#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _parser.py
# @Author:      Daniel Puente Ramírez
# @Time:        5/10/22 11:35

import pandas as pd

import variables as v
from av_parser.core.kiuwan.common import mapping_df


def parser(path, sep=','):
    """
    It takes a CSV file, filters it to only the columns we want, adds an ID column,
    maps the Priority and Software characteristic columns to the values Kiuwan
    wants, and renames the columns to the names Kiuwan wants

    :param path: the path to the file to be parsed
    :param sep: the separator used in the csv file, defaults to , (optional)
    :return: A dataframe with the columns and values that are needed for the Kiuwan
    report.
    """
    df = pd.read_csv(path, sep=sep)

    df = mapping_df(
        df,
        v.kiuwan.vuln_parse_columns,
        ['Priority',
         'Software characteristic'],
        [v.kiuwan.priority_map,
         v.kiuwan.software_characteristic_map])

    df.columns = v.kiuwan.vuln_excel_columns[:-1]

    return df
