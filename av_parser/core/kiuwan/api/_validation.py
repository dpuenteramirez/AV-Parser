#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    _validation.py
# @Author:      d3x3r
# @Time:        4/1/23 16:45

import variables as v
import sys
import requests


def kiuwan_validate_api_credentials():
    """It validates the Kiuwan API credentials."""
    v.log.info("Validating Kiuwan API credentials")
    url = v.kiuwan.api_urls_dict["base"] + v.kiuwan.api_urls_dict["info"]
    response = requests.get(url, auth=(v.kiuwan.username, v.kiuwan.password))
    if response.status_code == 200:
        v.log.success("Kiuwan API credentials are valid")
        v.log.info(
            "Remaining Quota: {}".format(response.headers["X-QuotaLimit-Remaining"])
        )
    else:
        v.log.failure(
            "Kiuwan API credentials are not valid. Please, "
            "check your credentials and try again."
        )
        sys.exit(1)
