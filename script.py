#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    script.py
# @Author:      Daniel Puente Ramírez
# @Time:        14/9/22 17:54

import os
from os.path import exists
import argparse
import textwrap
from tkinter.filedialog import askopenfilename

from utils.outputs import print_headers
from utils.splits import split_df

tmp_dir = 'tmp'
files = [
    'client',
    'scan_info',
    'risk',
    'vulns_per_host',
    'vulns_summary',
    'av-results-tmp',
    'av-results',
]



def create_tmp_dir():
    """
    Create a temporary directory
    :return: None
    """
    try:
        os.mkdir(tmp_dir)
        print('Created temporary directory')
    except FileExistsError:
        print('Temporary directory already exists. Skipping...')


def split_file(filepath):
    """
    Split the file in CSVs in order to be parsed more easily.
    :param filepath: Path to the file
    :return: Boolean
    """
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
                            os.path.join(tmp_dir, 'file_{}.csv'.format(
                                files[empty_lines])), 'w'
                    ) as f:
                        f.write(''.join(buffer))
                    buffer = []
                    empty_lines += 1

            else:
                mid_buffer = clear_line(buffer, line, mid_buffer)

            if empty_lines == 5:
                buffer = []
                mid_buffer = str()
                vulns_table = True
        else:
            buffer.append(line)

    with open(
            os.path.join(tmp_dir, 'file_{}.csv'.format(
                files[-2])), 'w'
    ) as f:
        f.write(''.join(buffer))

    split_df(os.path.join(tmp_dir, 'file_{}.csv'.format(files[-2])))

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


def main(filepath):
    """
    Main function
    :param filepath: Path to the file
    :return: None
    """
    create_tmp_dir()
    split_file(filepath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Vulnerability Analysis.')
    parser.add_argument('-f', '--file', type=str, help=textwrap.dedent('''\
           File to analyze.
           The file must be in the \'data\' directory 
           or a full path must be provided.
    '''))
    parser.add_argument('-G', '--gui', help='GUI mode.', action='store_true')
    parser.add_argument('-C', '--clear', help='Clear the tmp directory.',
                        action='store_true')
    args = parser.parse_args()

    base_file = str()

    if args.gui:
        base_file = askopenfilename()
        if not exists(base_file):
            print('File not found.\nExiting...')
            exit(1)
    elif args.file:
        if exists(args.file) or exists('data/' + args.file):
            print('Found file. Continuing...')
        else:
            print('File not found.\nExiting...')
            exit(1)
    else:
        parser.print_help()
        exit(1)

    # print_headers()

    main(filepath=args.file)

    if args.clear:
        print('Clearing temporary directory...')
        os.system('rm -rf tmp/')
