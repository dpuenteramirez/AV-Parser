#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _core.py
# @Author:      Daniel Puente Ramírez
# @Time:        14/9/22 17:54
import argparse
import os
import signal
import textwrap

from pwn import log
import variables as v

import utils

signal.signal(signal.SIGINT, utils.def_handler)


def _create_tmp_dir():
    """
    Create a temporary directory
    :return: None
    """
    try:
        os.mkdir(v.temp_dir)
        log.debug('Temporary directory created')
    except FileExistsError:
        log.debug('Temporary directory exists already')
    v.log.debug('Temporary directory: {}'.format(v.temp_dir))


def execute():
    """
    Control flow of the program.

    :return: None
    """
    parser = argparse.ArgumentParser(description='Vulnerability Analysis.')
    parser.add_argument('-f', '--file', type=str, help=textwrap.dedent('''\
                   File to analyze.
                   The file must be in the \'data\' directory 
                   or a full path must be provided.
            '''))
    parser.add_argument('-g', '--gui', help='GUI mode.', action='store_true')
    parser.add_argument('-o', '--output', help='Output file name.', type=str,
                        default='output.csv')
    parser.add_argument('-H', '--headers', help='Do not print headers.',
                        action='store_true')
    parser.add_argument('-l', '--log_level', help='Verbose mode.', type=str,
                        default='info')
    parser.add_argument('-C', '--clear', help='Force clear temporary files.',
                        action='store_true')
    args = parser.parse_args()

    if not args.headers:
        utils.print_headers()
    utils.parse_args(parser, args)

    _create_tmp_dir()
    utils.split_file(args.file)
    utils.create_excel()

    if args.clear:
        v.log.info('Clearing temporary files...')
        for f in os.listdir(v.temp_dir):
            os.remove(os.path.join(v.temp_dir, f))
        v.log.info('Temporary files cleared')

