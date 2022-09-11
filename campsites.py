#!/usr/bin/env python
import argparse
import copy
import requests
import curlify

import urllib
from urllib.parse import parse_qs
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Hardcoded list of campgrounds I'm willing to sleep at
PERMIT_NUMBER = {
    'Whitney': '233260'
}

WHITNEY_OPTIONS = {
    "overnight": "166",
    "day_use": "406"
}

# Runs the actual search
WHITNEY_PAYLOAD = {
    'commercial_acct': 'false'
}

BASE_URL = "https://www.recreation.gov/api/permits"


def find_availability(start_date, end_date, overnight=False):
    payload = generate_payload(start_date, end_date)

    division_number = WHITNEY_OPTIONS["day_use"]
    if overnight:
        division_number = WHITNEY_OPTIONS["overnight"]

    suffix = f"/{PERMIT_NUMBER['Whitney']}/divisions/{division_number}/availability"

    content_raw = send_request(payload, suffix)
    html = BeautifulSoup(content_raw, 'html.parser')
    # sites = get_site_list(html)
    # return sites
    print(content_raw)


def get_next_day(date):
    date_object = datetime.strptime(date, "%m-%d-%Y")
    next_day = date_object + timedelta(days=1)
    return datetime.strftime(next_day, "%m-%d-%Y")


def format_date(date):
    date_object = datetime.strptime(date, "%m-%d-%Y")
    date_formatted = datetime.strftime(date_object, "%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return date_formatted


def generate_payload(start, end):
    payload = copy.copy(WHITNEY_PAYLOAD)
    payload['start_date'] = format_date(start)
    payload['end_date'] = format_date(end)
    return payload


# def get_site_list(html):
#     sites = html.findAll('div', {"class": "check_avail_panel"})
#     results = []
#     for site in sites:
#         if site.find('a', {'class': 'book_now'}):
#             get_url = site.find('a', {'class': 'book_now'})['href']
#             # Strip down to get query parameters
#             get_query = get_url[get_url.find("?") + 1:] if get_url.find("?") >= 0 else get_url
#             if get_query:
#                 get_params = parse_qs(get_query)
#                 site_id = get_params['parkId']
#                 if site_id and site_id[0] in PARKS:
#                     results.append("%s, Booking Url: %s" % (PARKS[site_id[0]], BASE_URL + get_url))
#     return results


def send_request(payload, suffix=None):
    with requests.Session() as s:

        # s.get(BASE_URL, verify=False)  # Sets session cookie

        headers = {
            'User-Agent': 'Whitney-Bagger',
        }

        resp = s.get(BASE_URL + suffix, params=payload, verify=False, headers=headers)  # Runs search on specified dates

        if resp.status_code != 200:
            raise Exception("failedRequest",
                            f"ERROR, {resp.status_code} code received from {BASE_URL + suffix}")
        else:
            return resp.text


find_availability("09-08-2022", "09-10-2022")
