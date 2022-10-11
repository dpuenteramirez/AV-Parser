#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _parser.py
# @Author:      d3x3r
# @Time:        10/10/22 18:42

import os
import re

import pandas as pd

import variables as v

re_ipv4 = re.compile(r"(\"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\",)")


def parser(path):
    p_split = v.log.progress("Splitting file")
    f = open(path, "r")
    empty_lines = 0

    buffer_ = []
    mid_buffer = str()
    vulns_table = False
    for line in f:
        if not vulns_table:
            if not line.strip():
                if len(buffer_) > 0:
                    with open(
                            os.path.join(
                                v.temp_dir,
                                v.str["tmp_file_format"].format(
                                    v.files[empty_lines]),
                            ),
                            "w",
                    ) as f:
                        f.write("".join(buffer_))
                    buffer_ = []
                    empty_lines += 1
                    v.log.debug(v.str["file_created"].format(
                        v.files[empty_lines]))
                    p_split.status(v.str["file_created"].format(
                        v.files[empty_lines]))

            else:
                mid_buffer = _clear_line(buffer_, line, mid_buffer)

            if empty_lines == 5:
                buffer_ = []
                mid_buffer = str()
                vulns_table = True
        else:
            buffer_.append(line)

    with open(
            os.path.join(v.temp_dir,
                         v.str["tmp_file_format"].format(v.files[-2])),
            "w") as f:
        f.write("".join(buffer_))

    p_split.status("Creating DataFrame with vulns")
    _split_df(
        os.path.join(v.temp_dir, v.str["tmp_file_format"].format(v.files[-2])))

    df = pd.read_csv(os.path.join(v.temp_dir, v.files[-1] + ".csv"), sep="\t")
    df["Severity"] = df["Severity"].map(v.qualys.WAS.map_severity)
    df.to_csv(os.path.join(v.temp_dir, v.files[-1] + ".csv"),
              sep="\t",
              index=False)

    p_split.success(v.str["file_created"].format(v.files[-1]))

    v.log.success("File split successfully")

    with open(
            os.path.join(v.temp_dir,
                         v.str["tmp_file_format"].format(v.files[0])),
            "r") as f:
        _ = f.readline()
        line = f.readline()
        v.av_data.company = line.split(",")[0].replace('"', "")

    return True


def _clear_line(buffer, line, mid_buffer):
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
    file_ = open(filepath, "r")

    file_r = file_.read()
    r_newlines = "".join(file_r.splitlines())
    file_.close()
    chunks = re.split(re_ipv4, r_newlines)
    tmp = []
    str_tmp = ""
    for index, chunk in enumerate(chunks):
        if index % 2 == 0:
            line = str_tmp + chunk
            new_line = ""
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

    df.to_csv(os.path.join(v.temp_dir, v.files[-1] + ".csv"),
              index=False,
              sep="\t")
