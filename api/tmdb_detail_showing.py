from flask import Flask, request, Blueprint, jsonify
import requests
from flask_cors import CORS
import aiohttp  # 非同期HTTPリクエストを処理
import asyncio  # Pythonの非同期処理を管理


# Blueprint（APIのモジュール化）
detail_blueprint = Blueprint("detail", __name__)

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# CORSを有効化
CORS(app)

# TMDB APIの設定
TMDB_API_KEY = "55c13dc2187a4051c81a84bba6ec08f8"  # TMDBのAPIキー
TMDB_BASE_URL = "https://api.themoviedb.org/3/movie/"  # TMDBのベースURL


async def fetch(session, url, params):
    """非同期で API リクエストを送信"""
    async with session.get(
        url, params=params
    ) as response:  # 非同期のHTTPリクエストを送信
        return await response.json()


async def fetch_movie_details(movie_id):
    """映画の詳細・キャスト・おすすめ映画を並行取得"""
    # 複数のリクエストを管理
    async with aiohttp.ClientSession() as session:

        # URLの設定
        urls = {
            "details": f"{TMDB_BASE_URL}{movie_id}",
            "credits": f"{TMDB_BASE_URL}{movie_id}/credits",
            "recommendations": f"{TMDB_BASE_URL}{movie_id}/recommendations",
        }

        # パラメータ設定
        params = {"api_key": TMDB_API_KEY, "language": "ja-JP"}

        # タスクを準備（fetch() をキーと対応させた辞書を作成）
        # tasks = {
        #     "details": fetch(session, "https://api.themoviedb.org/3/movie/550", params),
        #     "credits": fetch(session, "https://api.themoviedb.org/3/movie/550/credits", params),
        #     "recommendations": fetch(session,"https://api.themoviedb.org/3/movie/550/recommendations",params,),
        # }
        tasks = {key: fetch(session, url, params) for key, url in urls.items()}

        # 並列処理したいコルーチンを asyncio.gather で並列処理
        # リストの各要素を個別の引数としてasyncio.gather()に渡す
        # 非同期処理（コルーチン）を同時に実行し、すべての結果が揃うのを待つ
        responses = await asyncio.gather(*tasks.values())

        # 取得結果を辞書化
        return dict(zip(tasks.keys(), responses))


@detail_blueprint.route("/", methods=["GET"])
def get_detail_movies():
    """映画の詳細・キャスト・おすすめ映画をまとめて取得"""

    # リクエストパラメータから検索条件を取得
    movie_id = request.args.get("movie_id")  # 映画ID

    # イベントループ設定
    loop = asyncio.new_event_loop()  # 新しいイベントループを作成
    asyncio.set_event_loop(loop)  # 引数loopをカレントイベントループに設定

    # 非同期処理を同期的に実行
    result = loop.run_until_complete(
        fetch_movie_details(movie_id)
    )  # 引数fetch_movie_details(movie_id)が完了するまで実行

    return jsonify(result)


# アプリケーションを実行
if __name__ == "__main__":
    app.run(debug=True)
