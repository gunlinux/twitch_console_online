import requests
import os
import sys

from dotenv import load_dotenv

load_dotenv()


class Liver:
    def __init__(self, token, refresh_token, client_id, app_secret):
        if not token:
            raise ValueError("where fuck is token")
        self.token = token
        self.client_id = client_id
        self.refresh_token = refresh_token
        self.app_secret = app_secret

    def _refresh(self):
        url = "https://id.twitch.tv/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "refresh_token",
            "client_secret": self.app_secret,
            "client_id": self.client_id,
            "refresh_token": self.refresh_token,
        }
        self._req(url=url, method="POST", headers=headers, data=data, refresh=True)

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
        if not data:
            return
        data = data[0]
        live = data.get('type', 'offline')
        if live != 'live':
            return
        print(f"On Air [{data.get('viewer_count', 0)}] 🐺")

    def _req(
        self, url, params=None, data=None, method="GET", headers=None, refresh=False
    ):
        if headers is None:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "CLient-Id": self.client_id,
            }
        req = requests.request(
            method=method, params=params, url=url, data=data, headers=headers
        )
        if req.status_code == 401 and not refresh:
            self._refresh()
            req = requests.request(
                method=method, params=params, url=url, data=data, headers=headers
            )
        if req.status_code == 200:
            return req.json()
        return


if __name__ == "__main__":
    user_id = '29122457'  # yoba eto ya
    if len(sys.argv) == 2:
        user_id = sys.argv[1]

    access_token = os.environ.get("ACCESS_TOKEN", "set_Dame_token")
    refresh_token = os.environ.get("REFRESH_TOKEN", "set_Dame_token")
    client_id = os.environ.get("CLIENT_ID", "set_Dame_token")
    app_secret = os.environ.get("APP_SECRET", "set_Dame_token")
    api = Liver(
        token=access_token,
        refresh_token=refresh_token,
        client_id=client_id,
        app_secret=app_secret,
    )
    api.get_live(user_id)
