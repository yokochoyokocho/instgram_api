import requests
import json
import datetime
import os
from pprint import pprint
from dotenv import load_dotenv
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial Unicode MS"]
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
    result = res["json_data"]

    items1 = result["data"][1]["values"]
    items2 = result["data"][2]["values"]
    items3 = result["data"][3]["values"]

    with open("insight_output.csv", "w", newline="") as csvFile:
        csvwriter = csv.writer(csvFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csvwriter.writerow(["date", "インプレッション", "プロフィールビュー", "リーチ"])
        dates = []

        impression = []
        profile_v = []
        reach = []

        for item1 in items1:
            impression.append(item1["value"])
            dates.append(item1["end_time"])
            csvwriter.writerow([item1["end_time"], item1["value"]])

        for item2 in items2:
            profile_v.append(item2["value"])
            csvwriter.writerow([item2["end_time"], item2["value"]])

        for item3 in items3:
            reach.append(item3["value"])
            csvwriter.writerow([item3["end_time"], item3["value"]])

    fig, ax1 = plt.subplots()
    # fig, ax2 = plt.subplots()
    # fig, ax3 = plt.subplots()

    # 折れ線グラフのデータ
    x = dates
    y1 = impression
    y2 = profile_v
    y3 = reach

    # 棒グラフに表示
    ax1.bar(x, y1, label="impression")
    ax1.bar(x, y2, label="プロフィールビュー")
    ax1.bar(x, y3, label="リーチ数")
    # 凡例（ラベル）の表示：左上に表示
    ax1.legend(loc="best")
    # ax2.legend(loc="best")
    # ax2.legend(loc="best")

    # グラフにタイトルをつける
    ax1.set_title("impression")
    # ax2.set_title("プロフィールビュー")
    # ax3.set_title("Daily insight")
    # x軸の軸ラベルを設定
    plt.xlabel("日")
    # y軸の軸ラベルを設定
    plt.ylabel("数")
    # グラフに表示
    plt.show()

    # 出力
    return res


# インスタグラム運用アカウントのインサイトを確認
def UserInsights(params, period, since, untill):
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
    Params["since"] = since
    Params["until"] = untill

    # エンドポイントURL
    url = params["endpoint_base"] + params["instagram_account_id"] + "/insights"  # endpoint url

    # 出力
    return InstaApiCall(url, Params, "GET")


day_since = "20230701"
day_untill = "20230720"

# day_since = input("データ取得の開始日を入力してください ＞ （）")
# day_untill = input("データ取得の終了日を入力してください ＞ ")
unix_since = datetime.datetime.strptime(day_since, "%Y%m%d")
unix_untill = datetime.datetime.strptime(day_untill, "%Y%m%d")

unix_since_output = int(unix_since.timestamp())
unix_untill_output = int(unix_untill.timestamp())

# メディア期間
period = "day"
since = unix_since_output
untill = unix_untill_output


# API呼出
params = basic_info()
response = UserInsights(params, period, since, untill)["json_data"]["data"]


# # 結果出力
# for insight in response:
#     print(insight["title"] + "（" + insight["description"] + ")" + " (" + insight["period"] + ")")
#     for value in insight["value"]:  # loop over each value
#         date_output = []
#         dte = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S+0000')
#         print(dte)
#         date_item = f"{dte.month}月{dte.day}日"
#         date_output.append(date_item)


# print("\t" + value["end_time"] + ": " + str(value["value"]))  # print out counts for the date
