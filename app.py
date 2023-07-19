import time
import requests
import json
import datetime
from pprint import pprint


# 別のファイルからほんとは呼び出したい
# from secret import module_token
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


# ここまで↑


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


# メディア作成
def createMedia(params):
    """
    ******************************************************************************************************
    【画像・動画コンテンツ作成】
    https://graph.facebook.com/v5.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access-token}
    https://graph.facebook.com/v5.0/{ig-user-id}/media?video_url={video-url}&caption={caption}&access_token={access-token}
    ******************************************************************************************************
    """
    # エンドポイントURL
    url = params["endpoint_base"] + params["instagram_account_id"] + "/media"
    # エンドポイント用パラメータ
    Params = dict()
    Params["caption"] = params["caption"]  # 投稿文
    Params["access_token"] = params["access_token"]  # アクセストークン
    # メディアの区分け
    if "IMAGE" == params["media_type"]:
        # 画像：メディアURLを画像URLに指定
        Params["image_url"] = params["media_url"]  # 画像URL
    else:
        # 動画：メディアURLを動画URLに指定
        Params["media_type"] = params["media_type"]  # メディアタイプ
        Params["video_url"] = params["media_url"]  # ビデオURL
    # 出力
    return InstaApiCall(url, Params, "POST")


# メディアID別ステータス管理
def getMediaStatus(mediaObjectId, params):
    """
    ******************************************************************************************************
    【APIエンドポイント】
    https://graph.facebook.com/v5.0/{ig-container-id}?fields=status_code
    ******************************************************************************************************
    """
    # エンドポイントURL
    url = params["endpoint_base"] + "/" + mediaObjectId
    # パラメータ
    Params = dict()
    Params["fields"] = "status_code"  # フィールド
    Params["access_token"] = params["access_token"]  # アクセストークン
    # 出力
    return InstaApiCall(url, Params, "GET")


# メディア投稿
def publishMedia(mediaObjectId, params):
    """
    ******************************************************************************************************
    【APIエンドポイント】
    https://graph.facebook.com/v5.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access-token}
    ******************************************************************************************************
    """
    # エンドポイントURL
    url = params["endpoint_base"] + params["instagram_account_id"] + "/media_publish"
    # エンドポイント送付用パラメータ
    Params = dict()
    Params["creation_id"] = mediaObjectId  # メディアID
    Params["access_token"] = params["access_token"]  # アクセストークン
    # 出力
    return InstaApiCall(url, Params, "POST")


# ユーザの公開レート制限・使用率を取得
def getContentPublishingLimit(params):
    """
    ******************************************************************************************************
    https://graph.facebook.com/v5.0/{ig-user-id}/content_publishing_limit?fields=config,quota_usage
    ******************************************************************************************************
    """
    # エンドポイントURL
    url = (
        params["endpoint_base"] + params["instagram_account_id"] + "/content_publishing_limit"
    )  # endpoint url
    # エンドポイント送付用のパラメータ
    Params = dict()
    Params["fields"] = "config,quota_usage"  # フィールド
    Params["access_token"] = params["access_token"]  # アクセストークン

    return InstaApiCall(url, Params, "GET")


# 画像投稿
def instagram_upload_image(media_url, media_caption):
    # パラメータ
    params = basic_info()
    params["media_type"] = "IMAGE"  # メディアType
    params["media_url"] = media_url  # メディアURL
    params["caption"] = media_caption

    # APIでメディア作成＆ID発行
    imageMediaId = createMedia(params)["json_data"]["id"]

    # メディアアップロード
    StatusCode = "IN_PROGRESS"
    while StatusCode != "FINISHED":
        # メディアステータス取得
        StatusCode = getMediaStatus(imageMediaId, params)["json_data"]["status_code"]
        # 待ち時間
        time.sleep(5)

    # Instagramにメディア公開
    publishImageResponse = publishMedia(imageMediaId, params)
    # 出力
    print("Instagram投稿完了")
    return publishImageResponse["json_data_pretty"]


# 【要修正】投稿内容
media_url = "https://photos.app.goo.gl/pXFV8FtA5YaUMJ3HA"  # 画像
media_caption = "あやちゃーん"  # 投稿文

# 関数実行
instagram_upload_image(media_url, media_caption)
