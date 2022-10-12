#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    __init__.py.py
# @Author:      d3x3r
# @Time:        6/10/22 16:28

import variables as v


def mapping_df(df, parse_columns, columns_to_map, mapping_dict):
    """It takes a dataframe, a list of columns to parse, a list of columns to
    map, and a list of dictionaries to map the columns to, and returns a
    dataframe with the columns mapped

    Parameters
    ----------
    df
        the dataframe to be mapped
    parse_columns
        the columns that you want to keep in the final dataframe
    columns_to_map
        a list of columns to map
    mapping_dict
        a list of dictionaries, each dictionary is a mapping for a column

    Returns
    -------
        A dataframe with the columns specified in parse_columns, with the
        columns specified in columns_to_map mapped to the values in the
        mapping_dict.

    """
    df = df.filter(items=parse_columns, axis=1)

    ids = [f"COD-{v.av_data.company}-{v.av_data.year}-"
           f"{str(int(v.av_data.starting_id) + i).zfill(6)}"
           for i in range(len(df))]

    df.insert(0, "ID", ids)

    for index, column in enumerate(columns_to_map):
        df[column] = df[column].map(mapping_dict[index])

    return df


def excel_col_format(df,
                     workbook,
                     worksheet,
                     bg_color,
                     criteria,
                     column_letter,
                     bold=True):
    """This function takes a dataframe, workbook, worksheet, background color,
    criteria, and column letter as inputs and formats the column letter in the
    worksheet with the background color and bold formatting
    if the criteria is met

    Parameters
    ----------
    df
        the dataframe you're working with
    workbook
        the workbook object
    worksheet
        the worksheet you're working with
    bg_color
        the background color of the cell
    criteria
        the criteria to be met for the formatting to be applied
    column_letter
        The column letter of the column you want to format.
    bold, optional
        True/False

    """
    formatting = workbook.add_format({
        "bold": bold,
        "bg_color": bg_color,
    })
    worksheet.conditional_format(
        f"{column_letter}{v.offset}:{column_letter}{len(df) + v.offset}",
        {
            "type": "formula",
            "criteria": f'=${column_letter}{v.offset}="{criteria}"',
            "format": formatting,
        },
    )
