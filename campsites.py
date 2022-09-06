#!/usr/bin/env python
import argparse
import copy
import requests

import urllib
from urllib.parse import parse_qs
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Hardcoded list of campgrounds I'm willing to sleep at
PARKS = {
    '70925': 'UPPER PINES',
    '70928': 'LOWER PINES',
    '70927': 'NORTH PINES',
    '73635': 'STANISLAUS',
    '70926': 'TUOLOMNE MEADOWS'
}

# Sets the search location to yosemite
LOCATION_PAYLOAD = {
    'currentMaximumWindow': '12',
    'locationCriteria': 'yosemite',
    'interest': '',
    'locationPosition': '',
    'selectedLocationCriteria': '',
    'resetAllFilters': 'false',
    'filtersFormSubmitted': 'false',
    'glocIndex': '0',
    'googleLocations': 'Yosemite National Park, Yosemite Village, CA 95389, USA|-119.53832940000001|37.8651011||LOCALITY'
}

# Sets the search type to camping
CAMPING_PAYLOAD = {
    'resetAllFilters': 'false',
    'filtersFormSubmitted': 'true',
    'sortBy': 'RELEVANCE',
    'category': 'camping',
    'selectedState': '',
    'selectedActivity': '',
    'selectedAgency': '',
    'interest': 'camping',
    'usingCampingForm': 'true'
}

# Runs the actual search
PAYLOAD = {
    'resetAllFilters': 'false',
    'filtersFormSubmitted': 'true',
    'sortBy': 'RELEVANCE',
    'category': 'camping',
    'availability': 'all',
    'interest': 'camping',
    'usingCampingForm': 'false'
}

BASE_URL = "https://www.recreation.gov"
UNIF_SEARCH = "/unifSearch.do"
UNIF_RESULTS = "/unifSearchResults.do"


def find_camp_sites(args):
    payload = generate_payload(args['start_date'], args['end_date'])

    content_raw = send_request(payload)
    html = BeautifulSoup(content_raw, 'html.parser')
    sites = get_site_list(html)
    return sites


def get_next_day(date):
    date_object = datetime.strptime(date, "%Y-%m-%d")
    next_day = date_object + timedelta(days=1)
    return datetime.strftime(next_day, "%Y-%m-%d")


def format_date(date):
    date_object = datetime.strptime(date, "%Y-%m-%d")
    date_formatted = datetime.strftime(date_object, "%a %b %d %Y")
    return date_formatted


def generate_payload(start, end):
    payload = copy.copy(PAYLOAD)
    payload['arrivalDate'] = format_date(start)
    payload['departureDate'] = format_date(end)
    return payload


def get_site_list(html):
    sites = html.findAll('div', {"class": "check_avail_panel"})
    results = []
    for site in sites:
        if site.find('a', {'class': 'book_now'}):
            get_url = site.find('a', {'class': 'book_now'})['href']
            # Strip down to get query parameters
            get_query = get_url[get_url.find("?") + 1:] if get_url.find("?") >= 0 else get_url
            if get_query:
                get_params = parse_qs(get_query)
                site_id = get_params['parkId']
                if site_id and site_id[0] in PARKS:
                    results.append("%s, Booking Url: %s" % (PARKS[site_id[0]], BASE_URL + get_url))
    return results


def     send_request(payload):
    with requests.Session() as s:

        s.get(BASE_URL + UNIF_RESULTS, verify=False)  # Sets session cookie
        s.post(BASE_URL + UNIF_SEARCH, LOCATION_PAYLOAD, verify=False)  # Sets location to yosemite
        s.post(BASE_URL + UNIF_SEARCH, CAMPING_PAYLOAD, verify=False)  # Sets search type to camping

        resp = s.post(BASE_URL + UNIF_SEARCH, payload, verify=False)  # Runs search on specified dates
        if resp.status_code != 200:
            raise Exception("failedRequest",
                            "ERROR, %d code received from %s".format(resp.status_code, BASE_URL + UNIF_SEARCH))
        else:
            return resp.text
