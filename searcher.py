#!/usr/bin/env python
import copy
import requests
from mailer import send_email_notification
from date_util import *

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

ACCEPTABLE_OVERNIGHT_DATES = [
    "10-07-2022",
    "10-08-2022",
    "10-09-2022",
    "10-14-2022",
    "10-15-2022",
    "10-16-2022",
    "10-21-2022",
    "10-22-2022",
    "10-23-2022"
]

ACCEPTABLE_DAY_USE_DATES = [
    "10-09-2022",
    "10-10-2022",
    "10-16-2022",
    "10-17-2022",
    "10-23-2022",
    "10-24-2022"
]


def find_availability(start_date, end_date, overnight=False):
    payload = generate_payload(start_date, end_date)

    division_number = WHITNEY_OPTIONS["day_use"]
    if overnight:
        division_number = WHITNEY_OPTIONS["overnight"]

    suffix = f"/{PERMIT_NUMBER['Whitney']}/divisions/{division_number}/availability"

    resp = send_request(payload, suffix)
    resp_json = resp.json()
    return resp_json["payload"]["date_availability"]


def generate_payload(start, end):
    payload = copy.copy(WHITNEY_PAYLOAD)
    payload['start_date'] = format_date_req(start)
    payload['end_date'] = format_date_req(end)
    return payload


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
            return resp


def search_acceptable_dates():
    day_use_availability = find_availability("10-07-2022", "10-24-2022")
    overnight_availability = find_availability("10-07-2022", "10-24-2022", overnight=True)

    avail_day_use = []
    avail_overnight = []

    for d in ACCEPTABLE_DAY_USE_DATES:
        date_info = day_use_availability[format_date_resp(d)]
        if date_info["remaining"] > 2 and s_to_d(d) > datetime.today():
            avail_day_use.append(f"{d} ({date_info['remaining']})")

    for d in ACCEPTABLE_OVERNIGHT_DATES:
        date_info = overnight_availability[format_date_resp(d)]
        if date_info["remaining"] > 2 and s_to_d(d) > datetime.today():
            avail_overnight.append(f"{d} ({date_info['remaining']})")

    if len(avail_day_use) > 0 or len(avail_overnight) > 0:
        print(f"Availability found! Overnight: {avail_overnight}, Day Use: {avail_day_use}")
        dates = {"day_use": avail_day_use, "overnight": avail_overnight}
        send_email_notification(dates)
    else:
        print("No availability... :(\nTrying again in 10 min.")


search_acceptable_dates()
