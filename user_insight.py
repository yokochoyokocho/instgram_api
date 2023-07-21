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


# インスタグラム運用アカウントのインサイトを確認
def UserInsights(params, period="day"):
    """
    ***********************************************************************************
    【APIエンドポイント】
    https://graph.facebook.com/{graph-api-version}/{ig-user-id}/insights?metric={metric}&period={period}
    ***********************************************************************************
    """
    # エンドポイントに渡すパラメータ
    Params = dict()
    Params[
        "metric"
    ] = "follower_count,impressions,profile_views,reach, get_directions_clicks, text_message_clicks, website_clicks, email_contacts, phone_call_clicks"  # インサイト指標
    Params["period"] = period  # 集計期間
    Params["access_token"] = params["access_token"]  # アクセストークン

    # エンドポイントURL
    url = params["endpoint_base"] + params["instagram_account_id"] + "/insights"  # endpoint url

    # 出力
    return InstaApiCall(url, Params, "GET")


# メディア期間
period = "day"

# API呼出
params = basic_info()
response = UserInsights(params, period)["json_data"]["data"]

# 結果出力
for insight in response:
    print(insight["title"] + "（" + insight["description"] + ")" + " (" + insight["period"] + ")")
    for value in insight["values"]:  # loop over each value
        print("\t" + value["end_time"] + ": " + str(value["value"]))  # print out counts for the date
