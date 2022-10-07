#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    __init__.py.py
# @Author:      d3x3r
# @Time:        5/10/22 11:22


class Kiuwan:
    vuln_excel_columns = [
        "ID",
        "CWE",
        "Criticidad",
        "Características del Software",
        "Código de la Regla",
        "Regla",
        "Lenguaje",
        "Archivo",
        "Número de Línea",
        "Texto de la Línea",
        "Archivo Fuente",
        "Número de Línea Fuente",
        "Texto de la Línea Fuente",
        "Framework",
        "Comentarios del Desarrollador",
    ]

    vuln_parse_columns = [
        "CWE",
        "Priority",
        "Software characteristic",
        "Rule code",
        "Rule",
        "Language",
        "File",
        "Line number",
        "Line text",
        "Source file",
        "Source line number",
        "Source line text",
        "Framework",
    ]

    priority_map = {
        "Very High": "Muy Alta",
        "High": "Alta",
        "Normal": "Normal",
        "Low": "Baja",
        "Very Low": "Muy Baja",
    }

    software_characteristic_map = {
        "Security": "Seguridad",
        "Reliability": "Fiabilidad",
        "Maintainability": "Mantenibilidad",
    }

    insights_excel_columns = [
        "ID",
        "Riesgo de seguridad",
        "Riesgo de obsolencia",
        "Riesgo de licencia",
        "Grupo",
        "Versión",
        "Nombre de archivo",
        "Lenguaje",
        "Licencias",
        "#Vulnerabilidades",
        "CVE",
        "Fuentes",
    ]

    insights_components_parse_columns = [
        "Security risk",
        "Obsolescence risk",
        "License risk",
        "Group",
        "Version",
        "Filename",
        "Language",
        "Licenses",
        "#Vulnerabilities",
        "CVE",
        "Sources",
    ]

    insights_map = {
        "High": "Alto",
        "Medium": "Medio",
        "Low": "Bajo",
        "None": "Ninguno",
        "Unknown": "Desconocido",
    }

    insights_license_parse_columns = [
        'License',
        'Component',
        'Associated by user',
        'Type',
        'SPDX code',
        'URL',
        'Risk',
        'Permissions',
        'Limitations',
        'Conditions',
    ]
