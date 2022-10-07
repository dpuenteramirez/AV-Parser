#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _cli.py
# @Author:      d3x3r
# @Time:        16/9/22 11:32
import os
import sys
from os.path import exists
from tkinter.filedialog import askopenfilename
import variables as v


def def_handler(_, __):
    v.log.failure('Exiting...')
    sys.exit(1)


def print_headers():
    folder = 'resources'
    with open(os.path.join(folder, 'av-parser_header.txt'), 'r') as f:
        print(f.read())

    print('by...', end='\n\n\n')

    with open(os.path.join(folder, 'd3x3r.txt'), 'r') as f:
        print(f.read())


def parse_args(parser, args):
    v.log.setLevel(args.log_level)

    if args.gui:
        base_file = askopenfilename()
        if not exists(base_file):
            v.log.failure('File not found.\nExiting...')
            exit(1)
    elif args.file:
        if exists(args.file) or exists('data/' + args.file):
            v.log.info('Found file. Starting...')
        else:
            v.log.failure('File not found.\nExiting...')
            exit(1)
    else:
        parser.print_help()
        exit(1)
