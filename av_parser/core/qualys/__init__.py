#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    __init__.py.py
# @Author:      d3x3r
# @Time:        5/10/22 11:22


class Qualys:
    class WAS:
        av_results = [
            "CVE ID",
            "Severity",
            "Category",
            "IP",
            "DNS",
            "OS",
            "Protocol",
            "Title",
            "Port",
            "SSL",
            "PCI Vuln",
            "Vendor Reference",
            "Impact",
            "Exploitability",
            "Solution",
            "Results",
        ]

        av_results_excel_columns = [
            "CVE",
            "Severidad",
            "Categoría",
            "Host",
            "DNS",
            "OS",
            "Protocolo",
            "Nombre",
            "Puerto",
            "SSL",
            "Afecta PCI",
            "Referencia Fabricante",
            "Impacto",
            "Exploitabilidad",
            "Solución",
            "Resultado",
        ]

        map_severity = {
            5: "Critical",
            4: "High",
            3: "Medium",
            2: "Low",
            1: "Info",
        }

        id_unique_vulns_excel_columns = [
            "ID Vuln Cliente",
            "Nombre",
            "Ocurrencias",
        ]

        host_severity_columns = [
            "IP",
            "Severity",
        ]

        host_severity_excel_columns = [
            "Host",
            "Info",
            "Low",
            "Medium",
            "High",
            "Critical",
        ]


    WAS = WAS()
