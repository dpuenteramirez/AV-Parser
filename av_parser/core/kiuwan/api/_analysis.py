#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _analysis.py
# @Author:      d3x3r
# @Time:        4/1/23 17:56

import variables as v
import requests
import sys
import pandas as pd


def kiuwan_api_control():
    """It controls the workflow in the Kiuwan API."""
    apps_dict = _get_applications()

    analysis = 0

    while analysis == 0:
        app_name = _select_application(apps_dict)
        analysis = _select_analysis(app_name)

    _get_vulnerabilities(app_name, analysis)


def _get_applications():
    """It gets the applications from the Kiuwan API."""
    v.log.info("Getting applications from the Kiuwan API")
    url = v.kiuwan.api_urls_dict["base"] + v.kiuwan.api_urls_dict["get_apps"]
    response = requests.get(url, auth=(v.kiuwan.username, v.kiuwan.password))

    if response.status_code == 200:
        v.log.success("Applications retrieved successfully")
        response_dict = response.json()
        response_dict.sort(key=lambda x: x["name"])

        return response_dict

    else:
        v.log.failure("Error retrieving applications")
        sys.exit(1)


def _select_application(apps_dict):
    """It selects the application to analyze.

    Parameters
    ----------
    apps_dict
        The dictionary with the applications.

    """
    print("Select the application to analyze:")
    for index, application in enumerate(apps_dict):
        print(f"{index + 1}. {application['name']}")

    while True:
        try:
            app_index = int(input("Select the application: "))
            if app_index not in range(1, len(apps_dict) + 1):
                raise ValueError
            break
        except ValueError:
            print("Please, enter a valid number.")

    v.log.success(f"Application selected: {apps_dict[app_index - 1]['name']}")

    return apps_dict[app_index - 1]["name"]


def _select_analysis(app_name):
    """It selects the analysis to analyze."""
    v.log.info("Getting analysis from the Kiuwan API")
    url = v.kiuwan.api_urls_dict["base"] + v.kiuwan.api_urls_dict[
        "get_analysis"
    ].format(app_name)

    response = requests.get(url, auth=(v.kiuwan.username, v.kiuwan.password))

    if response.status_code == 200:
        v.log.success("Analysis retrieved successfully")
        response_dict = response.json()

        response_dict.sort(key=lambda x: x["creationDate"], reverse=True)

        print("Select the analysis to analyze:")
        for index, analysis in enumerate(response_dict):
            print(
                f"{index + 1}. "
                f"{' '.join(analysis['creationDate'][:-1].split('T'))}"
                f" : Status {analysis['status']}"
                f" : Business Value {analysis['analysisBusinessValue']}"
            )
        print("0. Go back to the applications selection")

        while True:
            try:
                analysis_index = int(input("Select the analysis: "))
                if analysis_index not in range(0, len(response_dict) + 1):
                    raise ValueError
                break
            except ValueError:
                print("Please, enter a valid number.")

        if analysis_index == 0:
            return 0

        v.log.success(
            f"Analysis code selected:" f" {response_dict[analysis_index - 1]['code']}"
        )

        return response_dict[analysis_index - 1]["code"]

    else:
        v.log.failure(
            "Error retrieving analysis, are there any analysis for " "this application?"
        )
        return 0


def _get_vulnerabilities(app_name, analysis_code):
    """It gets the vulnerabilities from the Kiuwan API."""
    v.log.info("Getting vulnerabilities from the Kiuwan API")
    url = v.kiuwan.api_urls_dict["base"] + v.kiuwan.api_urls_dict[
        "get_defects_CSV_report"
    ].format(app_name, analysis_code)

    response = requests.get(url, auth=(v.kiuwan.username, v.kiuwan.password))

    if response.status_code == 200:
        v.log.success("Vulnerabilities retrieved successfully")

        with open(f"{v.temp_dir}/vulns.csv", "w") as f:
            f.write(response.text)

        vulns_df = pd.read_csv(f"{v.temp_dir}/vulns.csv", sep=",")

        print(vulns_df)

        print(vulns_df.keys())

        return 2

    else:
        print(response.headers)
        v.log.failure("Error retrieving vulnerabilities")
        sys.exit(1)
