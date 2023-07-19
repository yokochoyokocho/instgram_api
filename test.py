import requests
import json
import datetime
from pprint import pprint


def basic_info():
    # 初期
    config = dict()
    # 【要修正】アクセストークン
    config[
        "access_token"
    ] = "EABVRUXsUlVkBADaOW8VJQL7uoTU76vOYUDwFk1DRgBcw9WTWN7JMieRS9gSvtZCbli5MmTAvqFMT2Wsbc90biGqAEzGj3rpZCwYOJ8JGqsICN8T4P0Crk2Df2BRj8vNFIMpOju06UKPQJ2CjB5aV64n7xZBul1hNxKjCEafJpPTG7ZAdojxx"
    # 【要修正】アプリID
    config["app_id"] = "6000384910071129"
    # 【要修正】アプリシークレット
    config["app_secret"] = "8f9da64ca76578e9c1d781038aac89a3"
    # 【要修正】インスタグラムビジネスアカウントID
    config["instagram_account_id"] = "17841460786704613"
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


def debugAT(params):
    # エンドポイントに送付するパラメータ
    Params = dict()
    Params["input_token"] = params["access_token"]
    Params["access_token"] = params["access_token"]
    # エンドポイントURL
    url = params["graph_domain"] + "/debug_token"
    # 戻り値
    return InstaApiCall(url, Params, "GET")


# リクエスト
params = basic_info()  # リクエストパラメータ
response = debugAT(params)  # レスポンス

# レスポンス
pprint(response)
