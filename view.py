import os
import sys
import logging

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


class Liver:
    def __init__(self, token, client_id):
        self.token = token
        self.client_id = client_id

    def get_live(self, user_id):
        url = 'https://api.twitch.tv/helix/streams'
        params = {
            "user_id": user_id,
            "first": 1,
        }
        rez = api._req(url=url, params=params)
        if not rez or not rez['data']:
            return
        data = rez['data']

        live = data[0].get('type', 'offline')
        if live != 'live':
            return
        print(f"On Air [{data[0].get('viewer_count', 0)}] 🐺")

    def _req(self, url, params=None, data=None, method="GET", headers=None):
        if headers is None:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Client-Id": self.client_id,
            }
        req = requests.request(
            method=method, params=params, url=url, data=data, headers=headers
        )
        logger.critical(req.status_code)
        if req.status_code == 200:
            return req.json()
        return


if __name__ == "__main__":
    user_id = '29122457'
    logger.debug('start')
    if len(sys.argv) == 2:
        user_id = sys.argv[1]
    access_token = os.environ["ACCESS_TOKEN"]
    client_id = os.environ["CLIENT_ID"]
    api = Liver(token=access_token, client_id=client_id)
    api.get_live(user_id)
