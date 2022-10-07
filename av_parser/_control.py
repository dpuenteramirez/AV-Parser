#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _control.py
# @Author:      d3x3r
# @Time:        14/9/22 17:54
import argparse
import os
import signal
import textwrap

import pandas as pd
from pwn import log

import utils
import variables as v
from av_parser.core.kiuwan.insights import excel_components as kiuwan_insights_excel
from av_parser.core.kiuwan.insights import cli_license as kiuwan_cli_license
from av_parser.core.kiuwan.insights import parser_components as kiuwan_parser_components
from av_parser.core.kiuwan.insights import parser_security as kiuwan_parser_security
from av_parser.core.kiuwan.insights import parser_license as kiuwan_parser_license
from av_parser.core.kiuwan.insights import parser_obsolescence as \
    kiuwan_parser_obsolescence
from av_parser.core.kiuwan.vulnerabilities import excel as kiuwan_vuln_excel
from av_parser.core.kiuwan.vulnerabilities import parser as kiuwan_vuln_parser

signal.signal(signal.SIGINT, utils.def_handler)


def _create_tmp_dir():
    """It creates a temporary directory if it doesn't exist already."""
    try:
        os.mkdir(v.temp_dir)
        log.debug("Temporary directory created")
    except FileExistsError:
        log.debug("Temporary directory exists already")
    v.log.debug("Temporary directory: {}".format(v.temp_dir))


def execute():
    """It parses the command line arguments, creates a temporary directory,
    checks the parameters, and then calls the appropriate functions to parse
    the input file and create the output file.

    """
    parser = argparse.ArgumentParser(description="Vulnerability Analysis.")
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help=textwrap.dedent("""\
                   File to analyze.
                   The file must be in the \'data\' directory 
                   or a full path must be provided.
            """),
    )
    parser.add_argument("-g", "--gui", help="GUI mode.", action="store_true")
    parser.add_argument("-o",
                        "--output",
                        help="Output file name.",
                        type=str,
                        default="output")
    parser.add_argument("-H",
                        "--headers",
                        help="Do not print headers.",
                        action="store_true")
    parser.add_argument("-l",
                        "--log_level",
                        help="Verbose mode.",
                        type=str,
                        default="info")
    parser.add_argument("-C",
                        "--clear",
                        help="Force clear temporary files.",
                        action="store_true")
    parser.add_argument(
        "-F",
        "--format",
        help="Specify the input format. "
        "Currently supported: "
        "'qualys', 'kiuwan-vuln', "
        "'kiuwan-insights'.",
        type=str,
        default="kiuwan",
    )
    args = parser.parse_args()

    v.output = args.output

    if ".xlsx" not in v.output:
        v.output += ".xlsx"

    if not args.headers:
        utils.print_headers()
    utils.parse_args(parser, args)

    _create_tmp_dir()

    if _check_params():
        _input_base_data()
        log.info("Starting analysis...")
        if args.format == "qualys":
            utils.split_file(args.file)
            utils.control_excel_creation()

        if args.format == "kiuwan-vuln":
            df = kiuwan_vuln_parser(args.file)
            kiuwan_vuln_excel(df, v.output)

        if args.format == "kiuwan-insights":
            df = kiuwan_parser_components(args.file)
            kiuwan_insights_excel(df, v.output)

        if args.format == "kiuwan-insights-security":
            df = kiuwan_parser_security(args.file)
            # kiuwan_insights_excel(df, v.output)

        if args.format == "kiuwan-insights-license":
            df = kiuwan_parser_license(args.file)
            kiuwan_cli_license(df)

    if args.clear:
        v.log.info("Clearing temporary files...")
        for f in os.listdir(v.temp_dir):
            os.remove(os.path.join(v.temp_dir, f))
        v.log.info("Temporary files cleared")


def _check_params():
    v.log.debug("Checking parameters...")
    v.log.debug("All parameters OK")
    return True


def _input_base_data():
    """It asks the user for the company code, component, year and starting
    reference number.

    """
    if not _check_company_file():
        while len(v.av_data.company) != 3:
            company = input("Company Cod (3 chars): ")
            v.av_data.company = company.upper()[:3]

        while len(v.av_data.component) == 0:
            try:
                component = input("Component: ")
                v.av_data.component = component
            except ValueError:
                v.av_data.component = ""

        while v.av_data.year == 0:
            try:
                year = int(input("Year: "))
            except ValueError:
                year = 0
            v.av_data.set_year(year)

        try:
            starting_id = int(input("Starting ref (1, 2, ...): "))
        except ValueError:
            starting_id = 1
        v.av_data.starting_id = starting_id


def _check_company_file():
    """It checks if the company file exists, if it does, it loads the data
    into the variables

    Returns
    -------
        A boolean value.

    """
    v.log.info("Looking for company file...")
    required_columns = ["company cod", "component", "year", "starting id"]

    if not os.path.isfile("data/company.csv"):
        v.log.info("Company file not found. Asking for input...")
        return False

    try:
        company_data = pd.read_csv("data/company.csv")

        if len(company_data.columns) != 4:
            v.log.info("Company file is not valid. Asking for input...")
            return False

        if len(required_columns) == len(
                company_data.columns) and len(required_columns) == sum([
                    1 for i, j in zip(required_columns, company_data.columns)
                    if i == j
                ]):

            v.av_data.company = company_data["company cod"][0][:3]
            v.av_data.component = company_data["component"][0]
            v.av_data.set_year(company_data["year"][0])
            v.av_data.starting_id = int(company_data["starting id"][0])
            v.log.success("Company file found and loaded.")
            return True
        else:
            v.log.info("Company file is not valid. Asking for input...")
            return False

    except IndexError:
        v.log.info("Company file is empty or does not match the required "
                   "format. Please check data/company_example.csv for a valid "
                   "format example.")
        return False
