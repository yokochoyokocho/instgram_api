import os
import json
from instagram_graph_api import InstagramGraphApi
from dotenv import load_dotenv

load_dotenv()


def run():
    igapi = InstagramGraphApi()

    username = "username"  # ユーザー名
    business_account_id = os.getenv("BUSINESS_ACCOUNT_ID")  # ビジネスアカウントID
    access_token = os.getenv("ACCESS_TOKEN")  # アクセストークン

    # name: 表示名、username:ユーザー名、biography: プロフィール文、follows_count: フォロー数、followers_count: フォロワー数、media_count: メディア数
    user = igapi.fetch_user(
        username,
        business_account_id,
        access_token,
        "name,username,biography,follows_count,followers_count,media_count",
    )

    # impressions: ユーザーのメディアが閲覧された合計回数、reach: ユーザーのメディアを1つ以上閲覧したユニークユーザーの合計数、profile_views: ユーザーのプロフィールが閲覧された合計回数
    user_insight = igapi.fetch_user_insight(
        business_account_id, access_token, "impressions,reach,profile_views", "day"
    )

    user_info = {"user": user, "insight": user_insight}

    # timestamp: タイムスタンプ、caption: 本文、like_count: いいね数、comments_count: コメント数
    media = igapi.fetch_media(
        username,
        business_account_id,
        access_token,
        "timestamp,caption,like_count,comments_count,mediaproducttype,media_type",
    )

    media_info = []

    for media in media:
        # engagement: いいね数・コメント数・保存数の合計、reach: メディアを閲覧したユニークユーザーの合計数、impressions: メディアが閲覧された合計回数、saved: 保存数
        media_insight = igapi.fetch_media_insight(
            media["id"], access_token, "engagement,reach,impressions,saved"
        )

        media_info.append({"media": media, "insight": media_insight})

    print("【ユーザー情報】\n")
    print(json.dumps(user_info, ensure_ascii=False))

    print("\n------------------------\n")

    print("【メディア情報】\n")
    print(json.dumps(media_info, ensure_ascii=False))


if __name__ == "__main__":
    run()
