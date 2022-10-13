#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    __init__.py.py
# @Author:      d3x3r
# @Time:        5/10/22 11:22

obsolescence_risk = "Obsolescence risk"


class Kiuwan:
    """A class to interact with the Kiuwan Reports."""

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

    vulnerabilities_parse_columns = [
        "Rule code",
        "Rule",
        "Priority",
        "CWE",
        "Software characteristic",
        "Vulnerability type",
        "Language",
        "Effort",
        "File",
        "Line number",
        "Line text",
        "Source file",
        "Source line number",
        "Source line text",
        "Muted",
        "Normative",
        "Status",
        "CWE Scope",
        "Framework",
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
        "Portability": "Portabilidad",
        "Performance": "Rendimiento",
        "Usability": "Usabilidad",
        "Internationalization": "Internacionalización",
        "Accessibility": "Accesibilidad",
        "Interoperability": "Interoperabilidad",
        "Compliance": "Cumplimiento",
        "Other": "Otro",
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
        "Component",
        "Group",
        "Version",
        "Custom",
        "Filename",
        "Language",
        "#Licenses",
        "Licenses",
        "#Vulnerabilities",
        "CVE",
        obsolescence_risk,
        "License risk",
        "Security risk",
        " Sources",
    ]

    insights_comp_parse_columns = [
        "Security risk",
        obsolescence_risk,
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
        "License",
        "Component",
        "Associated by user",
        "Type",
        "SPDX code",
        "URL",
        "Risk",
        "Permissions",
        "Limitations",
        "Conditions",
    ]

    insights_obsolescence_parse_columns = [
        "Component",
        "Languaje",
        "Used version",
        "Custom",
        "Date",
        "Last version",
        "Date.1",
        "Releases",
        "Out of date",
        "Time inactivity",
        obsolescence_risk,
        "Risk",
    ]

    insights_security_parse_columns = [
        "CVE",
        "Private",
        "CWE",
        "Last modified",
        "Exploitability Subscore",
        "Impact Subscore",
        "CVSS v2 Base Score",
        "Description",
        "Attack vector(V2)",
        "Acces Complexity(V2)",
        "Authentication(V2)",
        "Confidentiality impact(V2)",
        "Integrity impact(V2)",
        "Availability impact(V2)",
        "vector(V2)",
        "Attack vector(V3)",
        "Access complexity(V3)",
        "Privileges Required(V3)",
        "User Interaction(V3)",
        "Scope(V3)",
        "Confidentiality impact(V3)",
        "Integrity impact(V3)",
        "Availability impact(V3)",
        "Component",
        "Mute",
    ]
