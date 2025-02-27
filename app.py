import os
from flask import Flask, send_from_directory, request, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from api.tmdb_currently_showing import movies_blueprint
from api.tmdb_popularity_showing import popularity_blueprint
from api.tmdb_rating_showing import rating_blueprint
from api.tmdb_search_showing import search_blueprint
from api.tmdb_detail_showing import detail_blueprint
from db.routes.auth_login import login_blueprint
from db.routes.create_user import createUser_blueprint
from db.database import init_db
import config

# Flask アプリの作成
app = Flask(__name__)

# CORS（Cross-Origin Resource Sharing）の設定
# CORS を有効化し、異なるドメインからのリクエストを許可
CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",
            "allow_headers": ["Content-Type", "Authorization"],
            "methods": ["GET", "POST", "OPTIONS"],
        }
    },
)

# 設定ファイルを読み込む
app.config.from_object("config.Config")
# DB初期化
init_db(app)

# 環境変数からJWT_SECRET_KEYを読み込む
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret_key")

# JWT（JSON Web Token）認証の設定
jwt = JWTManager(app)

# Blueprintを登録（ルーティングのモジュール化）
app.register_blueprint(movies_blueprint, url_prefix="/api/movies")
app.register_blueprint(popularity_blueprint, url_prefix="/api/popularity")
app.register_blueprint(rating_blueprint, url_prefix="/api/rating")
app.register_blueprint(search_blueprint, url_prefix="/api/search")
app.register_blueprint(detail_blueprint, url_prefix="/api/detail")
app.register_blueprint(login_blueprint, url_prefix="/login")
app.register_blueprint(createUser_blueprint, url_prefix="/createUser")


# サーバーのルート
@app.route("/")
def serve():
    # プロジェクトのルートディレクトリを取得
    project_root = os.path.abspath(os.path.dirname(__file__))
    # templates フォルダから index.html を提供
    return send_from_directory(os.path.join(project_root, "templates"), "index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")


# @app.route("/<path:path>")
# def static_files(path):
#     return send_from_directory(app.static_folder, path)

# アプリの起動
if __name__ == "__main__":
    # 開発
    app.run(debug=True)
    # 本番
    # port = int(os.environ.get('PORT', 8080))  # 環境変数PORTがあれば使用
    # serve(app, host='0.0.0.0', port=port)
