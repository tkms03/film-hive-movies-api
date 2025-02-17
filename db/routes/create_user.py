from flask import Flask, request, Blueprint, jsonify, make_response, abort
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from db.services.auth_login_service import authenticate
from db.services.create_user_servise import create_user

createUser_blueprint = Blueprint("createUser", __name__)

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# # CORSの設定を追加
CORS(app)


# ログイン認証
@createUser_blueprint.route("", methods=["POST", "OPTIONS"])
def createUser():

    if request.method == "OPTIONS":
        response = jsonify({"message": "OK"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        return response, 200

    # クライアントから送信されたデータを取得
    input_data = request.get_json()
    if not input_data:
        abort(400, description="無効なリクエスト形式です。JSON本文が必要です。")

    # データからuser_id、passwordを取得
    user_id = input_data.get("user_id")
    user_name = input_data.get("user_name")
    password = input_data.get("password")
    if not user_id or not user_name or not password:
        abort(400, description="ユーザIDまたはユーザ名またはパスワードがありません。")

    # 新規ユーザ作成
    new_user = create_user(user_id, user_name, password)
    if new_user is None:
        abort(400, description="すでにユーザが存在しています。")

    # JWTを生成
    access_token = create_access_token(identity=new_user.user_id)

    # JWTをクライアントに返す
    return jsonify(access_token=access_token), 200
