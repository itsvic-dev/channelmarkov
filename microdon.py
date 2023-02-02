import requests
import secrets
import pickle
import base64
import os
import time

class MastodonOAuth2:
    state = secrets.token_urlsafe(32)
    code_challenge = secrets.token_urlsafe(32)
    scopes = ["write:statuses"]

    def __init__(self, name: str, instance: str, client_id: str, client_secret: str):
        self.name = name
        self.instance = instance
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_header = "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    def fetch_access_token(self):
        url = (f"{self.instance}/oauth/authorize?response_type=code&client_id={self.client_id}&redirect_uri=urn:ietf:wg:oauth:2.0:oob" +
            f"&scope={'+'.join(self.scopes)}&force_login=true")

        print("Open this URL in your browser:")
        print(url)
        code = input("Then copy and paste the authorization code after logging in: ")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "code": code,
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
            "scope": ' '.join(self.scopes)
        }

        resp = requests.post(f"{self.instance}/oauth/token", headers=headers, data=data)

        json = resp.json()
        self.access_token = json["access_token"]

    def check_auth(self):
        if not os.path.exists(f"{self.name}.pickle"):
            self.fetch_access_token()
            with open(f"{self.name}.pickle", "wb+") as auth:
                pickle.dump({
                    "access_token": self.access_token,
                }, auth)
        else:
            with open(f"{self.name}.pickle", "rb") as auth:
                auth_data = pickle.load(auth)
                self.access_token = auth_data["access_token"]

    def send_toot(self, content: str):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        json = {
            "status": content
        }

        resp = requests.post(f"{self.instance}/api/v1/statuses", headers=headers, json=json)
        if resp.status_code != 200:
            raise Exception(f"Failed to send toot: {resp.status_code} ({resp.text})")
