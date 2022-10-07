#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    __init__.py.py
# @Author:      Daniel Puente Ramírez
# @Time:        5/10/22 11:23

from ._output import (excel)
from ._parser import (parser)

__all__ = [
    'parser',
    'excel',
]
