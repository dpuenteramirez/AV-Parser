#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    __init__.py.py
# @Author:      Daniel Puente Ramírez
# @Time:        5/10/22 15:34

from datetime import date


class AVData:
    company = ''
    component = ''
    year = 0
    starting_id = 1
    auditor = 'Mnemo'
    audit_date = str(date.today().strftime('%d-%m-%Y'))
    version = '1.0'

    def set_year(self, year):
        if len(str(year)) == 4:
            self.year = year
        elif len(str(year)) == 2:
            self.year = '20' + str(year)
        else:
            self.year = date.today().year
