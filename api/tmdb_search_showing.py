from flask import Flask, request, Blueprint, jsonify
import requests
from flask_cors import CORS

search_blueprint = Blueprint('search', __name__)

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# # CORSの設定を追加
CORS(app)

# TMDBのAPIキーを設定
TMDB_API_KEY = '55c13dc2187a4051c81a84bba6ec08f8'
TMDB_BASE_URL = 'https://api.themoviedb.org/3/discover/movie?'

@search_blueprint.route('/', methods=['GET'])
def get_search_movies():
    
  # リクエストパラメータから検索条件を取得
  page = request.args.get('page')   # ページ数
  # keywords = request.args.get('keyword')   #キーワード
  minRating = request.args.get('minRating')   # 評価（最小）
  maxRating = request.args.get('maxRating')   # 評価（最大）
  minVotes = request.args.get('minVotes')   # 投票数（最小）
  maxVotes = request.args.get('maxVotes')   # 投票数（最大）
  releaseYearFrom = request.args.get('releaseYearFrom')   # 公開年（FROM）
  releaseYearTo = request.args.get('releaseYearTo')   # 公開年（TO）
  genres = request.args.get('genres')   # ジャンル

  # TMDBに送信するパラメータ
  params = {
    'api_key': TMDB_API_KEY,
    'sort_by': 'vote_average.desc', # 評価順（降順）
    # 'with_keywords': keywords,
    'vote_average.gte': minRating,
    'vote_average.lte': maxRating ,
    'vote_count.gte': minVotes,
    'vote_count.lte': maxVotes,
    'primary_release_date.gte':releaseYearFrom,
    'primary_release_date.lte':releaseYearTo,
    'with_genres':genres,
    'language': 'ja-JP',  # 日本語の結果を取得
    'page': page,
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
    app.run(debug=false)