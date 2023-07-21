from time import sleep
import requests
import textwrap

BASE_URL = "https://graph.facebook.com/v11.0"  # APIのバージョンを指定


class InstagramGraphApi:
    def __init__(self):
        self.base_url = BASE_URL

    # ユーザーを取得
    def fetch_user(self, username, business_account_id, access_token, data_fields):
        url = f"{self.base_url}/{business_account_id}"
        fields = f"business_discovery.username({username}){{{data_fields}}}"
        params = {"fields": fields, "access_token": access_token}

        return requests.get(url, params=params).json()["business_discovery"]

    # メディアを取得
    def fetch_media(self, username, business_account_id, access_token, data_fields):
        url = f"{self.base_url}/{business_account_id}"
        fields = f"business_discovery.username({username}){{media{{{data_fields}}}}}"
        params = {"fields": fields, "access_token": access_token}

        res = requests.get(url, params=params).json()["business_discovery"]

        media = []

        for i in range(len(res["media"]["data"])):
            media.append(res["media"]["data"][i])

        # Instagram Graph APIの仕様上、一度のリクエストで取得できるのは25件までなので、それ以上取得したい場合は複数回リクエストを送る
        if "after" in res["media"]["paging"]["cursors"].keys():
            after = res["media"]["paging"]["cursors"]["after"]

            while after is not None:
                url = f"{self.base_url}/{business_account_id}"
                fields = f"business_discovery.username({username}){{media.after({after}){{{data_fields}}}}}"
                params = {"fields": fields, "access_token": access_token}

                res = requests.get(url, params=params).json()["business_discovery"]

                for i in range(len(res["media"]["data"])):
                    media.append(res["media"]["data"][i])

                if "after" in res["media"]["paging"]["cursors"].keys():
                    after = res["media"]["paging"]["cursors"]["after"]
                else:
                    after = None

                sleep(1)  # API制限にかからないよう適度に時間を空ける

        return media

    # インサイト（ユーザー）を取得
    def fetch_user_insight(self, business_account_id, access_token, metric, period):
        url = f"{self.base_url}/{business_account_id}/insights"
        params = {"metric": metric, "period": period, "access_token": access_token}

        return requests.get(url, params=params).json()["data"]

    # インサイト（メディア）を取得
    def fetch_media_insight(self, media_id, access_token, metric):
        url = f"{self.base_url}/{media_id}/insights"
        params = {"metric": metric, "access_token": access_token}

        return requests.get(url, params=params).json()["data"]
