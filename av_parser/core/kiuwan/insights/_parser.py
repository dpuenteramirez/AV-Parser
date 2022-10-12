#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _parser.py
# @Author:      d3x3r
# @Time:        6/10/22 11:20

import sys

import pandas as pd

import variables as v
from av_parser.core.kiuwan.common import mapping_df
from av_parser.core.common import check_csv


def parser_components(path, sep=","):
    """It reads the file, cleans it up, and then maps the columns to the
    correct values

    Parameters
    ----------
    path
        the path to the file to parse
    sep, optional
        the separator used in the file.

    Returns
    -------
        A dataframe with the columns:
        - 'File', '#Vulnerabilities', 'Security risk', 'Obsolescence risk',
        'License risk'

    """
    check_csv(path)
    with open(path, "r") as f:
        columns = f.readline()
        n_columns = columns.count(sep)
        columns = [c.lstrip() for c in columns.strip().split(sep)]

    cleaned_lines = _cleanup(path, n_columns, sep)
    df = pd.DataFrame(cleaned_lines, columns=columns)

    try:
        df = mapping_df(
            df,
            v.kiuwan.insights_comp_parse_columns,
            ["Security risk", "Obsolescence risk", "License risk"],
            [v.kiuwan.insights_map] * 3,
        )
    except KeyError:
        v.log.failure(
            "Format not recognized. Please check the file format "
            "and/or the input parametrization."
        )
        sys.exit(1)

    df["#Vulnerabilities"] = df["#Vulnerabilities"].astype(int)

    df.columns = v.kiuwan.insights_excel_columns

    return df


def parser_security(path, sep=","):
    """It reads a CSV file and returns a Pandas dataframe

    Parameters
    ----------
    path
        The path to the file to be parsed.
    sep, optional
        The separator used in the CSV file.

    Returns
    -------
        A dataframe

    """
    check_csv(path)

    df = pd.read_csv(path, sep=sep)

    v.log.info("Parsing security file")

    return df


def parser_obsolescence(path, sep=","):
    """This function reads in a csv file, filters out the rows that are not
    "High" or "Medium" risk, and returns a dataframe with only the "Risk" column

    Parameters
    ----------
    path
        the path to the csv file
    sep, optional
        the separator used in the CSV file.

    Returns
    -------
        A dataframe with the risk column and only the rows that have a risk of
        high or medium.

    """
    check_csv(path)

    df = pd.read_csv(path, sep=sep)

    df = df[["Risk"]]

    options = ["High", "Medium"]
    df = df.loc[df["Risk"].isin(options)]

    return df


def parser_license(path, sep=","):
    """It reads in a CSV file, filters out the rows that don't have a risk of
    "high" or "medium", and returns a dataframe with only the columns "Risk",
    "SPDX code", and "Component"

    Parameters
    ----------
    path
        the path to the CSV file
    sep, optional
        The separator used in the CSV file.

    Returns
    -------
        A dataframe with the columns Risk, SPDX code, and Component.

    """
    check_csv(path)

    df = pd.read_csv(path, sep=sep)

    df = df[["Risk", "SPDX code", "Component"]]

    options = ["high", "medium"]
    df = df.loc[df["Risk"].isin(options)]

    return df


def _cleanup(path, n_columns, sep):
    """It reads in a file, splits each line by the separator, and then checks
    to see if the number of columns is correct. If it is, it adds the line to a
    list of cleaned lines

    Parameters
    ----------
    path
        the path to the file you want to clean
    n_columns
        the number of columns in the file
    sep
        the separator used in the file

    Returns
    -------
        A list of lists.

    """
    cleaned_lines = []

    check_csv(path)
    with open(path, "r") as f:
        lines = f.readlines()

        for _, line in enumerate(lines[1:]):
            line = line.strip()

            if _n_line_seps(line, sep) == n_columns:
                cleaned_lines.append(_split_line_by_sep_no_quotes(line, sep))

    return cleaned_lines


def _n_line_seps(line, sep):
    """It counts the number of times the separator character appears in the
    line, but only if it's not inside a pair of double quotes.

    Parameters
    ----------
    line
        the line of text to be parsed
    sep
        the separator character

    Returns
    -------
        The number of times the separator is found in the line.

    """
    inside_quotes = False
    n_seps = 0
    for char in line:
        if char == '"':
            inside_quotes = not inside_quotes
        elif char == sep and not inside_quotes:
            n_seps += 1

    return n_seps


def _split_line_by_sep_no_quotes(line, sep):
    """It splits a string by a separator, but ignores the separator if it's
    inside quotes.

    Parameters
    ----------
    line
        the line to be split
    sep
        The character used to separate the values in the file.

    Returns
    -------
        A list of strings.

    """
    new_line = []
    inside_quotes = False
    text = ""
    for char in line:
        if char == '"':
            inside_quotes = not inside_quotes
        elif char == sep and not inside_quotes:
            new_line.append(text)
            text = ""
        else:
            text += char

    new_line.append(text)

    return new_line
