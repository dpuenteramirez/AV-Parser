#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _parser.py
# @Author:      d3x3r
# @Time:        5/10/22 11:35

import os
import sys

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
    _languages_tmp()
    if not bool(path.endswith(".csv")):
        v.log.error(f'The file "{path}" is not a csv file.')
        sys.exit(1)

    df = pd.read_csv(path, sep=sep)

    df_vuln_type = df["Vulnerability type"].copy()

    df_vuln_type = df_vuln_type.value_counts()
    df_vuln_type.to_csv(
        os.path.join(v.temp_dir, "vuln_type.csv"), index=True, header=True
    )
    v.log.debug(
        f"Vulnerability type file created\n\tPath: "
        f"{os.path.join(v.temp_dir, 'vuln_type.csv')}"
    )

    try:
        df = mapping_df(
            df,
            v.kiuwan.vuln_parse_columns,
            ["Priority", "Software characteristic"],
            [v.kiuwan.priority_map, v.kiuwan.software_characteristic_map],
        )
    except KeyError:
        v.log.failure(
            "Format not recognized. Please check the file format "
            "and/or the input parametrization."
        )
        sys.exit(1)

    df.columns = v.kiuwan.vuln_excel_columns[:-1]

    return df


def _languages_tmp():
    """
    It creates a CSV file with the list of languages in the Kiuwan
    """
    if len(v.kiuwan.languages) > 0:
        df = pd.DataFrame(
            v.kiuwan.languages.values(),
            index=v.kiuwan.languages.keys(),
            columns=["Language"],
        )
        df.to_csv(os.path.join(v.temp_dir, "languages.csv"), index=True, header=True)
        v.log.debug(
            f"Languages file created\n\tPath: "
            f"{os.path.join(v.temp_dir, 'languages.csv')}"
        )
