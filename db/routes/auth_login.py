from flask import Flask, request, Blueprint, jsonify, make_response, abort
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from db.services.auth_login_service import authenticate

import logging

logging.basicConfig(level=logging.DEBUG)
login_blueprint = Blueprint("login", __name__)

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# # CORSの設定を追加
CORS(app)


# ログイン認証
@login_blueprint.route("", methods=["POST", "OPTIONS"])
def login():

    if request.method == "OPTIONS":
        response = jsonify({"message": "OK"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        return response, 200

    try:
        # クライアントから送信されたデータを取得
        input_data = request.get_json()

        # データが不足している場合、エラー
        if not input_data:
            abort(400, description="無効なリクエスト形式です。JSON本文が必要です。")

        # 必須パラメータのチェック
        user_id = input_data.get("user_id")
        password = input_data.get("password")
        if not input_data or not input_data:
            abort(400, description="ユーザIDまたはパスワードがありません。")

        # ユーザー認証
        auth_user = authenticate(user_id, password)
        if auth_user is None:
            abort(401, description="無効なユーザー資格情報です。")

        # JWTを生成
        access_token = create_access_token(identity=auth_user.user_id)

        # JWTをクライアントに返す
        return jsonify(access_token=access_token), 200

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        abort(500, description="Internal Server Error")
