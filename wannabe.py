import re
import requests
import logging


class wannabe(object):
    """Wannabe5 Client"""

    def __init__(self, **args):
        self.event_id = args['event_id']
        self.api_url = args['api_url']
        self.client_id = args['client_id']
        self.client_secret = args['client_secret']

        self.token_url = "{}/auth/services/login".format(self.api_url)
        self.token = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.login()

    def login(self):
        payload = {
            'client_secret': self.client_secret,
            'client_id': self.client_id,
            'grant_type': 'client_credentials'
        }
        r = requests.post(self.token_url, data=payload)
        if(r.status_code != 200):
            self.logger.error(
                "Failed to login to Wannabe. Got status code: {}"
                .format(r.status_code)
            )
            raise Exception("Failed to login to Wannabe")

        self.token = r.json()['access_token']

    def request(self, method, path, data=None):
        url = "{}/{}".format(self.api_url, path)
        cookies = dict(wannabe_jwt=self.token)
        r = requests.request(
            method,
            url,
            cookies=cookies,
            json=data
        )
        if(r.status_code != 200):
            self.logger.error(
                "Request failed to {} Got status code: {}"
                .format(url, r.status_code)
            )
            raise Exception("API request failed")
        return r.json()

    def get_lists(self, domain):
        wb_maillist = {}

        lists = self.request(
            'GET', 'communication/lists?per_page=100'  # TODO Add event check
        )['data']

        for list in lists:
            if list['identifier'].split('@')[1] == domain:
                wb_maillist.update({list['identifier'].lower(): list})
        return wb_maillist

    def get_members_of_list(self, list):
        print(list['id'])
        recipients = self.request(
            'GET', 'communication/lists/{}/recipients'.format(list['id'])
        )['values']
        members = []
        for data in recipients:
            user_email = re.sub(r'(\+.*?)(?=\@)', '', data['email'].lower())
            members.append(user_email)
        return members
