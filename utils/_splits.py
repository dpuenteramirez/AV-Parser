#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _splits.py
# @Author:      d3x3r
# @Time:        15/9/22 18:23

import variables as v
import pandas as pd
import re
import os

re_ipv4 = re.compile(r"(\"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\",)")


def split_file(filepath):
    """
    Split the file in CSVs in order to be parsed more easily.
    :param filepath: Path to the file
    :return: Boolean
    """
    p_split = v.log.progress('Splitting file')
    f = open(filepath, 'r')
    empty_lines = 0

    buffer = []
    mid_buffer = str()
    vulns_table = False
    for line in f:
        if not vulns_table:
            if not line.strip():
                if len(buffer) > 0:
                    with open(
                            os.path.join(v.temp_dir,
                                         v.str['tmp_file_format'].format(
                                             v.files[empty_lines])), 'w'
                    ) as f:
                        f.write(''.join(buffer))
                    buffer = []
                    empty_lines += 1
                    v.log.debug(
                        v.str['file_created'].format(v.files[empty_lines])
                    )
                    p_split.status(
                        v.str['file_created'].format(v.files[empty_lines])
                    )

            else:
                mid_buffer = clear_line(buffer, line, mid_buffer)

            if empty_lines == 5:
                buffer = []
                mid_buffer = str()
                vulns_table = True
        else:
            buffer.append(line)

    with open(
            os.path.join(v.temp_dir, v.str['tmp_file_format'].format(
                v.files[-2])), 'w'
    ) as f:
        f.write(''.join(buffer))

    p_split.status('Creating DataFrame with vulns')
    split_df(os.path.join(v.temp_dir,
                          v.str['tmp_file_format'].format(v.files[-2])))
    p_split.success(v.str['file_created'].format(v.files[-1]))
    return True


def clear_line(buffer, line, mid_buffer):
    if line.count('"') % 2 == 0:
        line = line.replace('"', '')
        buffer.append(line)
    else:
        mid_buffer += line
        if mid_buffer.count('"') % 2 == 0:
            mid_buffer = mid_buffer.replace('"', '').replace('\n',
                                                             ' ')
            buffer.append(mid_buffer)
            mid_buffer = str()
    return mid_buffer


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

    os.remove(filepath)
    v.log.debug(v.str['file_deleted'].format(v.files[-2]))

    df.to_csv(os.path.join(v.temp_dir, v.files[-1]+'.csv'), index=False,
              sep='\t')
