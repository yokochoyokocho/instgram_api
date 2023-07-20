import time
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


def get_hashtag_id(hashtag_word):
    """
    ***********************************************************************************
    【APIのエンドポイント】
    https://graph.facebook.com/{graph-api-version}/ig_hashtag_search?user_id={user-id}&q={hashtag-name}&fields={fields}
    ***********************************************************************************
    """
    # リクエスト
    Params = basic_info()  # リクエストパラメータ
    Params["hashtag_name"] = hashtag_word  # ハッシュタグ情報

    # エンドポイントに送付するパラメータ
    Params["user_id"] = Params["instagram_account_id"]  # インスタユーザID
    Params["q"] = Params["hashtag_name"]  # ハッシュタグ名
    Params["fields"] = "id,name"  # フィールド情報
    url = Params["endpoint_base"] + "ig_hashtag_search"  # エンドポイントURL

    # レスポンス
    response = InstaApiCall(url, Params, "GET")

    sample = response["json_data"]
    print(sample)
    # 戻り値（ハッシュタグID）
    return response["json_data"]["data"][0]["id"]


def get_hashtag_media_top(params, hashtag_id):
    """
    ***********************************************************************************
    【APIのエンドポイント】
    https://graph.facebook.com/{graph-api-version}/{ig-hashtag-id}/top_media?user_id={user-id}&fields={fields}
    ***********************************************************************************
    """
    # パラメータ
    Params = dict()
    Params["user_id"] = params["instagram_account_id"]
    Params["fields"] = "id,children,caption,comment_count,like_count,media_type,media_url,permalink"
    Params["access_token"] = params["access_token"]

    # エンドポイントURL
    url = params["endpoint_base"] + hashtag_id + "/" + "top_media"

    return InstaApiCall(url, Params, "GET")


# 【要修正】検索したいハッシュタグワードを記述
hashtag_word = "平泉"

# ハッシュタグIDを取得
hashtag_id = get_hashtag_id(hashtag_word)

# パラメータセット
params = basic_info()

# ハッシュタグ情報取得
hashtag_response = get_hashtag_media_top(params, hashtag_id)

# 出力
print("「" + hashtag_word + "」のハッシュタグID: " + str(hashtag_id))
for post in hashtag_response["json_data"]["data"]:
    print("\n\n---------- トップメディア ----------\n")
    print("ID: " + post["id"])
    print("\n投稿リンク: " + post["permalink"])
    try:
        print("\nいいね数: " + str(post["like_count"]))
    except:
        pass
    print("\n投稿文:")
    print(post["caption"])
    print("\nメディアタイプ:")
    print(post["media_type"])
