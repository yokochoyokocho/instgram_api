import requests
import json
import datetime
import os
from pprint import pprint
from dotenv import load_dotenv


load_dotenv()


def basic_info():
    # 初期
    config = dict()
    # 【要修正】アクセストークン
    config["access_token"] = os.environ["Access_token"]
    # 【要修正】アプリID
    config["app_id"] = os.environ["App_id"]
    # 【要修正】アプリシークレット
    config["app_secret"] = os.environ["App_secret"]
    # 【要修正】インスタグラムビジネスアカウントID
    config["instagram_account_id"] = os.environ["Instagram_account_id"]
    # 【要修正】グラフバージョン
    config["version"] = "v17.0"
    # 【修正不要】graphドメイン
    config["graph_domain"] = "https://graph.facebook.com/"
    # 【修正不要】エンドポイント
    config["endpoint_base"] = config["graph_domain"] + config["version"] + "/"
    # 出力
    return config


# APIリクエスト用の関数
def InstaApiCall(url, params, request_type):
    # リクエスト
    if request_type == "POST":
        # POST
        req = requests.post(url, params)
    else:
        # GET
        req = requests.get(url, params)

    # レスポンス
    res = dict()
    res["url"] = url
    res["endpoint_params"] = params
    res["endpoint_params_pretty"] = json.dumps(params, indent=4)
    res["json_data"] = json.loads(req.content)
    res["json_data_pretty"] = json.dumps(res["json_data"], indent=4)

    # 出力
    return res


def get_user_media_stats(params, ig_user_name):
    """
    ***********************************************************************************
    【APIのエンドポイント】
    "https://graph.facebook.com/v14.0/17841405309211844?fields=business_discovery.username('ig_username'){followers_count,media_count}&access_token={access-token}"
    ***********************************************************************************
    """

    # エンドポイントに送付するパラメータ
    Params = dict()
    Params["user_id"] = params["instagram_account_id"]
    Params["access_token"] = params["access_token"]
    Params["fields"] = (
        "business_discovery.username("
        + ig_username
        + "){followers_count,media_count,media{comments_count,like_count}}"
    )
    # エンドポイントURL
    url = params["endpoint_base"] + Params["user_id"]
    # 出力
    return InstaApiCall(url, Params, "GET")


# 【要修正】インスタグラムユーザー名を指定！
ig_username = "hiraizumi_contents_trial"

# リクエストパラメータ
params = basic_info()  # リクエストパラメータ
response = get_user_media_stats(params, ig_username)  # レスポンス

# 出力
pprint(response)
