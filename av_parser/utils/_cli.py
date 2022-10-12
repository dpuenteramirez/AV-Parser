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
    """It prints a message to the screen and exits the program

    Parameters
    ----------
    _
        The signal number
    __
        The name of the command.

    """
    v.log.failure("Exiting...")
    sys.exit(1)


def print_headers():
    """It prints the header and the author's name

    """
    folder = "resources"
    with open(os.path.join(folder, "av-parser_header.txt"), "r") as f:
        print(f.read())

    print("by...", end="\n\n\n")

    with open(os.path.join(folder, "d3x3r.txt"), "r") as f:
        print(f.read())


def parse_args(parser, args):
    """It checks if the file exists, and if it doesn't, it exits the program

    Parameters
    ----------
    parser
        The parser object that was created in the main function.
    args
        The arguments passed to the program.

    """
    v.log.setLevel(args.log_level)

    if args.gui:
        base_file = askopenfilename()
        args.file = base_file
        if not exists(base_file):
            v.log.failure("File not found.\nExiting...")
            sys.exit(1)
    elif args.file:
        if exists(args.file) or exists("data/" + args.file):
            v.log.info("Found file. Starting...")
        else:
            v.log.failure("File not found.\nExiting...")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)
