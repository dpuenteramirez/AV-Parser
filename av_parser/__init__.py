#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    __init__.py.py
# @Author:      Daniel Puente Ramírez
# @Time:        16/9/22 12:42


import variables as v
from pwn import *

from ._core import (execute)

__all__ = ["execute", "create_runtime"]


def create_runtime():
    v.start()
    v.temp_dir = tempfile.mkdtemp()
    v.log = log
    v.files = [
        'client',
        'scan_info',
        'risk',
        'vulns_per_host',
        'vulns_summary',
        'av-results-tmp',
        'av-results',
    ]
    v.str = {
        'scan_info': 'Scan Information',
        'risk': 'Risk',
        'vulns_per_host': 'Vulnerabilities per Host',
        'vulns_summary': 'Vulnerabilities Summary',
        'file_created': 'File created: {}',
        'file_deleted': 'File deleted: {}',
        'tmp_file_format': 'file_{}.csv',
    }

