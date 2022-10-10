#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    __init__.py.py
# @Author:      d3x3r
# @Time:        16/9/22 12:42

from pwn import *

import variables as v
from ._control import execute
from .core.av_data import AVData
from .core.kiuwan import Kiuwan
from .core.qualys import Qualys

__all__ = ["execute", "create_runtime"]


def create_runtime():
    """It creates the runtime environment for the script."""
    v.start()
    v.temp_dir = tempfile.mkdtemp()
    v.log = log
    v.files = [
        "client",
        "scan_info",
        "risk",
        "vulns_per_host",
        "vulns_summary",
        "av-results-tmp",
        "av-results",
    ]
    v.str = {
        "scan_info": "Scan Information",
        "risk": "Risk",
        "vulns_per_host": "Vulnerabilities per Host",
        "vulns_summary": "Vulnerabilities Summary",
        "file_created": "File created: {}",
        "file_deleted": "File deleted: {}",
        "tmp_file_format": "file_{}.csv",
    }

    v.offset = 15

    v.kiuwan = Kiuwan()
    v.qualys = Qualys()
    v.av_data = AVData()
