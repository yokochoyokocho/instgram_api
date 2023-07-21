import requests
import json
import datetime
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()


def get_instagram_insights(access_token):
    api_url = "https://graph.facebook.com/v12.0/me/media"
    params = {
        "fields": "id,media_type,like_count,comment_count,insights.metric(impressions,reach,engagement)",
        "access_token": access_token,
    }

    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("エラーが発生しました:", e)
        return None


if __name__ == "__main__":
    # アクセストークンを取得して、以下に設定してください
    access_token = os.environ["Access_token"]
    insights_data = get_instagram_insights(access_token)
    print(insights_data)
