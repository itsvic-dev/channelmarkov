import requests
import secrets
import pickle
import base64
import os
import time

class TwitterOAuth2:
    state = secrets.token_urlsafe(32)
    code_challenge = secrets.token_urlsafe(32)
    redirect_uri = "https://omame.xyz/test"
    scopes = ["tweet.read", "tweet.write", "users.read", "offline.access"]

    def __init__(self, name: str, client_id: str, client_secret: str):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_header = "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    def fetch_access_token(self):
        url = ("https://twitter.com/i/oauth2/authorize?response_type=code&" +
                f"client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope=" +
                "%20".join(self.scopes) + f"&state={self.state}&code_challenge=" +
                self.code_challenge + "&code_challenge_method=plain")

        print("Open this URL in your browser:")
        print(url)
        response_url = input("Then copy and paste the URL after logging in: ")

        code = response_url.split("code=")[1]

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": self.authorization_header
        }

        data = {
            "code": code,
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "code_verifier": self.code_challenge,
        }

        resp = requests.post("https://api.twitter.com/2/oauth2/token", headers=headers, data=data)

        json = resp.json()
        self.access_token = json["access_token"]
        self.refresh_token = json["refresh_token"]
        self.expires_at = time.time() + json["expires_in"]

    def renew_access_token(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": self.authorization_header
        }

        data = {
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
            "client_id": self.client_id
        }

        resp = requests.post("https://api.twitter.com/2/oauth2/token", headers=headers, data=data)
        json = resp.json()
        self.access_token = json["access_token"]
        self.refresh_token = json["refresh_token"]
        self.expires_at = time.time() + json["expires_in"]

    def check_auth(self):
        if not os.path.exists(f"{self.name}.pickle"):
            self.fetch_access_token()
            with open(f"{self.name}.pickle", "wb+") as auth:
                pickle.dump({
                    "access_token": self.access_token,
                    "refresh_token": self.refresh_token,
                    "expires_at": self.expires_at,
                    "state": self.state,
                    "code_challenge": self.code_challenge
                }, auth)
        else:
            with open(f"{self.name}.pickle", "rb") as auth:
                auth_data = pickle.load(auth)
                self.state = auth_data["state"]
                self.code_challenge = auth_data["code_challenge"]
                self.expires_at = auth_data["expires_at"]
                if time.time() > self.expires_at:
                    self.refresh_token = auth_data["refresh_token"]
                    self.renew_access_token()
                    with open(f"{self.name}.pickle", "wb+") as auth:
                        pickle.dump({
                            "access_token": self.access_token,
                            "refresh_token": self.refresh_token,
                            "expires_at": self.expires_at,
                            "state": self.state,
                            "code_challenge": self.code_challenge
                        }, auth)
                else:
                    self.access_token = auth_data["access_token"]

    def send_tweet(self, content: str):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        json = {
            "text": content
        }

        resp = requests.post("https://api.twitter.com/2/tweets", headers=headers, json=json)
        if resp.status_code != 201:
            raise Exception(f"Failed to send tweet: {resp.status_code} ({resp.text})")
