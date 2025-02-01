from flask import Flask, request, Blueprint, jsonify
import requests
from flask_cors import CORS

rating_blueprint = Blueprint('rating', __name__)

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# # CORSの設定を追加
CORS(app)

# TMDBのAPIキーを設定
TMDB_API_KEY = '55c13dc2187a4051c81a84bba6ec08f8'
TMDB_BASE_URL = 'https://api.themoviedb.org/3/discover/movie?'

@rating_blueprint.route('/', methods=['GET'])
def get_rating_movies():
    
  # リクエストパラメータから検索条件を取得
  page = request.args.get('page')   # ページ数

  # TMDBに送信するパラメータ
  params = {
    'api_key': TMDB_API_KEY,
    'sort_by': 'vote_average.desc', # 評価順（降順）
    'page': page,
    'language': 'ja-JP'  # 日本語の結果を取得
  }
  
  # APIを呼び出す
  response = requests.get(TMDB_BASE_URL, params=params)


  if response.status_code == 200:
    # 成功時にJSONデータを返す
    return jsonify(response.json())
    # return jsonify(response.json())
  else:
    # エラー時にエラーメッセージを返す
    return jsonify({'error': 'Failed to fetch data from TMDB'}), response.status_code

# アプリケーションを実行
if __name__ == '__main__':
    # debug=Trueを指定すると、エラー時にデバッグ情報が表示され、開発時に便利です。
    # ただし、本番環境ではdebug=Falseに設定してください。
    app.run(debug=True)