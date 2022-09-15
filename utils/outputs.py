#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    outputs.py
# @Author:      Daniel Puente Ramírez
# @Time:        15/9/22 11:43

import os


def print_headers():
    folder = 'resources'
    with open(os.path.join(folder, 'av-parser_header.txt'), 'r') as f:
        print(f.read())

    print('by...', end='\n\n\n')

    with open(os.path.join(folder, 'd3x3r.txt'), 'r') as f:
        print(f.read())
