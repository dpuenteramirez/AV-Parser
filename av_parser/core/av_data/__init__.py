#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    __init__.py.py
# @Author:      d3x3r
# @Time:        5/10/22 15:34

from datetime import date


class AVData:
    """A class to interact with the common data and the company."""

    company = ""
    component = ""
    year = 0
    starting_id = 1
    auditor = "Mnemo"
    audit_date = str(date.today().strftime("%d-%m-%Y"))
    version = "1.0"

    def set_year(self, year):
        """If the year is a 4-digit number, set the year to that number. If
        the year is a 2-digit number, set the year to 20 plus that number.
        Otherwise, set the year to the current year.

        Parameters
        ----------
        year
            The year of the data you want to download.

        """
        if len(str(year)) == 4:
            self.year = year
        elif len(str(year)) == 2:
            self.year = "20" + str(year)
        else:
            self.year = date.today().year
