import copy
import requests
from query_helper import *


class Query:
    base_url = "https://www.recreation.gov/api/"

    additional_payload = {
        'commercial_acct': 'false'
    }

    def __init__(self, permit_id, month, ):
        self.permit_id = permit_id
        self.start_date, self.end_date = get_month_dates(month)
        self.response = None

    def generate_payload(self):
        payload = copy.copy(Query.additional_payload)
        payload['start_date'] = self.start_date
        payload['end_date'] = self.end_date
        return payload

    def send_request(self, suffix=None):
        with requests.Session() as s:
            headers = {
                'User-Agent': 'Whitney-Bagger',
            }

            resp = s.get(Query.base_url + suffix, params=self.generate_payload(), verify=False, headers=headers)  # Runs search on specified dates

            if resp.status_code != 200:
                raise Exception("failedRequest",
                                f"ERROR, {resp.status_code} code received from {Query.base_url + suffix}")
            else:
                self.response = resp

    def get_response(self):
        resp_json = self.response.json()
        return resp_json["payload"]


