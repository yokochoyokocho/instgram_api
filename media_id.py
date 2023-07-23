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


def getUserMedia(params, pagingUrl=""):
    """
    ***************************************************************************************
    【APIのエンドポイント】
    https://graph.facebook.com/{graph-api-version}/{ig-user-id}/media?fields={fields}&access_token={access-token}
    ***************************************************************************************
    """
    # エンドポイントに渡すパラメータ
    Params = dict()
    Params["fields"] = "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username"  # フィールド
    Params["access_token"] = os.environ["Access_token"]  # アクセストークン

    if pagingUrl == "":
        # 先頭のページリンク取得
        url = params["endpoint_base"] + params["instagram_account_id"] + "/media"
    else:
        # 特定のページリンク取得
        url = pagingUrl

    # 出力
    return InstaApiCall(url, Params, "GET")


# パラメータ
params = basic_info()


# 結果出力（先頭ページ）
response = getUserMedia(params)
# いらない
test = response["json_data"]
print(test)

print("\n----------" + str(response["json_data"]["data"][0]["username"]) + "の投稿内容 ----------\n")
for i, post in enumerate(response["json_data"]["data"]):
    print("\n----------投稿内容(" + str(i + 1) + ")----------\n")
    print("投稿日: " + post["timestamp"])
    print("投稿メディアID: " + post["id"])
    print("メディア種別: " + post["media_type"])
    print("投稿リンク: " + post["permalink"])
    print("\n投稿文: " + post["caption"])

# 結果出力（2ページ目）
try:
    response = getUserMedia(params, response["json_data"]["paging"]["next"])
    print("\n----------" + str(response["json_data"]["data"][0]["username"]) + "の投稿内容 ----------\n")
    for i, post in enumerate(response["json_data"]["data"]):
        # print("\n----------投稿内容(" + str(i + 1) + ")----------\n")
        print("投稿日: " + post["timestamp"])
        print("投稿メディアID: " + post["id"])
        # print("メディア種別: " + post["media_type"])
        # print("投稿リンク: " + post["permalink"])
        # print("\n投稿文: " + post["caption"])
except:
    pass
