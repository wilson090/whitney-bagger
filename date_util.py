from datetime import *


def s_to_d(d):
    return datetime.strptime(d, "%m-%d-%Y")


def format_date_req(d):
    date_object = s_to_d(d)
    date_formatted = datetime.strftime(date_object, "%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return date_formatted


def format_date_resp(d):
    date_object = s_to_d(d)
    date_formatted = datetime.strftime(date_object, "%Y-%m-%dT%H:%M:%SZ")
    return date_formatted

