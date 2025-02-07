import os
from flask import Flask, send_from_directory, request, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from api.tmdb_currently_showing import movies_blueprint
from api.tmdb_popularity_showing import popularity_blueprint
from api.tmdb_rating_showing import rating_blueprint
from api.tmdb_search_showing import search_blueprint
from auth.auth_login import login_blueprint

app = Flask(__name__, static_folder="./frontend/build", static_url_path="")
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
# api = Api(app, doc="/documents/")


# 環境変数からJWT_SECRET_KEYを読み込む
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret_key")
jwt = JWTManager(app)

# Blueprintを登録
app.register_blueprint(movies_blueprint, url_prefix="/api/movies")
app.register_blueprint(popularity_blueprint, url_prefix="/api/popularity")
app.register_blueprint(rating_blueprint, url_prefix="/api/rating")
app.register_blueprint(search_blueprint, url_prefix="/api/search")
app.register_blueprint(login_blueprint, url_prefix="/auth/login")


@app.route("/")
def serve():
    # Flask はデフォルトで templates フォルダを探しに行くので、index.html は templates フォルダ内に置くべき
    return render_template("index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    # 開発
    app.run(debug=True)
    # 本番
    # port = int(os.environ.get('PORT', 8080))  # 環境変数PORTがあれば使用
    # serve(app, host='0.0.0.0', port=port)
