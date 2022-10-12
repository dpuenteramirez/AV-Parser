#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    variables.py
# @Author:      d3x3r
# @Time:        16/9/22 12:37


def start():
    # PYL-W0601 - It's a global variable
    global root_dir, temp_dir, log, files, str, output, kiuwan, qualys, av_data, offset
    root_dir = None
    temp_dir = None
    log = None
    files = None
    str = None  # PYL-W0622 - It's a global variable
    output = None
    kiuwan = None
    qualys = None
    av_data = None
    offset = None
