#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _parser.py
# @Author:      d3x3r
# @Time:        10/10/22 18:42

import os
import re
import sys

import pandas as pd

import variables as v

re_ipv4 = re.compile(r"(\"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\",)")


def parser(path):
    """It splits the file into two files, one with the vulnerabilities table and
     the other with the rest of the data

    Parameters
    ----------
    path
        The path to the file to be parsed.

    """
    if not bool(path.endswith(".csv")):
        v.log.error(f"The file \"{path}\" is not a csv file.")
        sys.exit(1)

    p_split = v.log.progress("Splitting file")
    f = open(path, "r")
    empty_lines = 0

    buffer_ = []
    mid_buffer = str()
    vulns_table = False
    for line in f:
        if not vulns_table:
            buffer_, empty_lines = _line_appears_ok(
                buffer_, empty_lines, line, mid_buffer, p_split
            )

            if empty_lines == 5:
                buffer_ = []
                mid_buffer = str()
                vulns_table = True
        else:
            buffer_.append(line)

    with open(
        os.path.join(v.temp_dir, v.str["tmp_file_format"].format(v.files[-2])), "w"
    ) as f:
        f.write("".join(buffer_))

    p_split.status("Creating DataFrame with vulns")
    _split_df(os.path.join(v.temp_dir, v.str["tmp_file_format"].format(v.files[-2])))

    df = pd.read_csv(os.path.join(v.temp_dir, v.files[-1] + ".csv"), sep="\t")
    df["Severity"] = df["Severity"].map(v.qualys.WAS.map_severity)
    df.to_csv(os.path.join(v.temp_dir, v.files[-1] + ".csv"), sep="\t", index=False)

    p_split.success(v.str["file_created"].format(v.files[-1]))

    v.log.success("File split successfully")

    with open(
        os.path.join(v.temp_dir, v.str["tmp_file_format"].format(v.files[0])), "r"
    ) as f:
        _ = f.readline()
        line = f.readline()
        v.av_data.company = line.split(",")[0].replace('"', "")


def _line_appears_ok(buffer_, empty_lines, line, mid_buffer, p_split):
    """If the line is empty, write the buffer to a file and clear the buffer.
    If the line is not empty, clear the line

    Parameters
    ----------
    buffer_
        The buffer that holds the lines of the file.
    empty_lines
        The number of empty lines that have been encountered.
    line
        the current line of the file
    mid_buffer
        a list of lines that are in the middle of a paragraph
    p_split
        the progress bar

    Returns
    -------
        buffer_, empty_lines

    """
    if not line.strip():
        if len(buffer_) > 0:
            with open(
                os.path.join(
                    v.temp_dir,
                    v.str["tmp_file_format"].format(v.files[empty_lines]),
                ),
                "w",
            ) as f:
                f.write("".join(buffer_))
            buffer_ = []
            empty_lines += 1
            v.log.debug(v.str["file_created"].format(v.files[empty_lines]))
            p_split.status(v.str["file_created"].format(v.files[empty_lines]))

    else:
        _clear_line(buffer_, line, mid_buffer)
    return buffer_, empty_lines


def _clear_line(buffer, line, mid_buffer):
    """If the line has an even number of quotes, then it's a complete line,
    so we append it to the buffer. If it has an odd number of quotes,
    then it's an incomplete line, so we append it to the mid_buffer. If the
    mid_buffer has an even number of quotes, then it's a complete line,
    so we append it to the buffer

    Parameters
    ----------
    buffer
        This is the list that will hold the lines of the file.
    line
        the current line of the file
    mid_buffer
        This is a string that will hold the line if it's not complete.

    Returns
    -------
        A list of strings.

    """
    if line.count('"') % 2 == 0:
        line = line.replace('"', "")
        buffer.append(line)
    else:
        mid_buffer += line
        if mid_buffer.count('"') % 2 == 0:
            mid_buffer = mid_buffer.replace('"', "").replace("\n", " ")
            buffer.append(mid_buffer)
            mid_buffer = str()
    return mid_buffer


def _split_df(filepath):
    """It takes a filepath, reads the file, splits the file into chunks,
    splits the chunks into lines, and then writes the lines to a csv file

    Parameters
    ----------
    filepath
        the path to the file to be split

    """
    if not bool(filepath.endswith(".csv")):
        v.log.error(f"The file \"{filepath}\" is not a csv file.")
        sys.exit(1)

    with open(filepath, "r") as file_:
        file_r = file_.read()
        r_newlines = "".join(file_r.splitlines())

    chunks = re.split(re_ipv4, r_newlines)
    tmp = []
    str_tmp = ""
    for index, chunk in enumerate(chunks):
        if index % 2 == 0:
            line = str_tmp + chunk
            new_line = ""
            new_line = _split_line(line, new_line)
            new_line = new_line.split(",")
            tmp.append(new_line)
            str_tmp = ""
        else:
            str_tmp += chunk

    df = pd.DataFrame(tmp)
    df = df.replace('"', "", regex=True)
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])

    os.remove(filepath)
    v.log.debug(v.str["file_deleted"].format(v.files[-2]))

    df.to_csv(os.path.join(v.temp_dir, v.files[-1] + ".csv"), index=False, sep="\t")


def _split_line(line, new_line):
    """It replaces commas with semicolons, but only if the comma is not inside
    a pair of double quotes

    Parameters
    ----------
    line
        the line to be split
    new_line
        the new line that will be written to the new file

    Returns
    -------
        A new line with the commas replaced with semicolons.

    """
    for index_c, c in enumerate(line):
        if c == ",":
            if line[index_c - 1] not in ['"', ","]:
                new_line += ";"
            else:
                new_line += c
        elif c == '"':
            if line[index_c - 1] == '"':
                new_line += ""
            else:
                new_line += c
        else:
            new_line += c
    return new_line
