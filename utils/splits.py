#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    splits.py
# @Author:      Daniel Puente Ramírez
# @Time:        15/9/22 18:23

import pandas as pd
import re

re_ipv4 = "(\"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\",)"
re_split = "(,,|\"\,\")"

def split_df(filepath):
    file = open(filepath, 'r')

    file_r = file.read()
    r_newlines = "".join(file_r.splitlines())
    file.close()
    chunks = re.split(re_ipv4, r_newlines)
    tmp = []
    str_tmp = ''
    for index, chunk in enumerate(chunks):
        if index % 2 == 0:
            line = (str_tmp + chunk)
            new_line = ''
            for index_c, c in enumerate(line):
                if c == ',':
                    if line[index_c - 1] not in ['"', ',']:
                        new_line += ';'
                    else:
                        new_line += c
                elif c == '"':
                    if line[index_c - 1] == '"':
                        new_line += ''
                    else:
                        new_line += c
                else:
                    new_line += c
            new_line = new_line.split(',')
            tmp.append(new_line)
            str_tmp = ''
        else:
            str_tmp += chunk

    df = pd.DataFrame(tmp)
    df = df.replace('\"', '', regex=True)
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])

    return df



