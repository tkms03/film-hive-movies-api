from flask import Flask, request, Blueprint, jsonify, make_response
from flask_cors import CORS
from flask_jwt_extended import create_access_token

import logging

logging.basicConfig(level=logging.DEBUG)
login_blueprint = Blueprint("login", __name__)

# CORSの設定を追加
CORS(login_blueprint)


# ユーザ情報（仮データ
users = [
    {
        "user_id": "U0000001",
        "login_id": "user1",
        "password": "12345678",
        "name": "山田太郎",
    },
    {
        "user_id": "U0000002",
        "login_id": "user2@example.com",
        "password": "password456",
        "name": "鈴木一郎",
    },
    {
        "user_id": "U0000003",
        "login_id": "user3@example.com",
        "password": "password789",
        "name": "斉藤花子",
    },
]


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

        if (
            not input_data
            or "login_id" not in input_data
            or "password" not in input_data
        ):
            return make_response(jsonify({"message": "Invalid request format."}), 400)

        auth_user = authenticate(input_data.get("login_id"), input_data.get("password"))

        if auth_user is None:
            return make_response(jsonify({"message": "Invalid User."}), 401)

        # JWTを生成
        access_token = create_access_token(identity=auth_user["user_id"])
        # JWTをクライアントに返す
        return make_response(jsonify({"access_token": access_token}), 200)

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return make_response(jsonify({"message": "Internal Server Error"}), 500)


# ユーザ認証関数
def authenticate(login_id, password):
    auth_user = next(
        (
            user
            for user in users
            if (user.get("login_id") == login_id and user.get("password") == password)
        ),
        None,
    )
    return auth_user
