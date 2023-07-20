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
    if request_type == 'POST' :
        # POST
        req = requests.post(url,params)
    else :
        # GET
        req = requests.get(url,params)
    
    # レスポンス
    res = dict()
    res["url"] = url
    res["endpoint_params"]        = params
    res["endpoint_params_pretty"] = json.dumps(params, indent=4)
    res["json_data"]              = json.loads(req.content)
    res["json_data_pretty"]       = json.dumps(res["json_data"], indent=4)
    
    # 出力
    return res


# 特定のメディアIDを指定しインサイトを確認
def MediaInsights(params, media_id, media_type) :
    """
    ***********************************************************************************
    【APIエンドポイント】
    https://graph.facebook.com/{graph-api-version}/{ig-media-id}/insights?metric={metric}
    ***********************************************************************************
    """
    # エンドポイントに渡すパラメータ
    Params = dict()
    if media_type == 'VIDEO':
        # 動画の場合
        Params['metric'] = 'engagement,impressions,reach,saved,video_views'             # 動画インサイト指標
    elif media_type == "REEL":
        # Reelの場合
        Params['metric'] = 'comments,likes,reach,saved,plays,shares,total_interactions' # リールインサイト指標
    elif media_type == 'STORY':
        # ストーリーの場合
        Params['metric'] = 'exits,impressions,reach,replies,taps_forward,taps_back'     # ストーリーインサイト指標
    else:
        # 写真の場合
        Params['metric'] = 'engagement,impressions,reach,saved'                         # 写真インサイト指標
    
    Params['access_token'] = params['access_token']                                     # アクセストークン
    
    # エンドポイントURL
    url = params['endpoint_base'] + media_id + '/insights'
    
    # 出力
    return InstaApiCall(url, Params, 'GET')


# 【要修正】メディアID
media_id   = 'XXXXX'
# 【要修正】メディア種別（IMAGE or VIDEO or STORY or REEL）
media_type = 'IMAGE'

# API呼出
params   = basic_info()
response = MediaInsights(params, media_id, media_type)['json_data']['data']

# 結果出力 
for insight in response:
    print (insight['title'] + "（" + insight['description'] + ")")
    print (">> " + str(insight["values"][0]["value"]))
