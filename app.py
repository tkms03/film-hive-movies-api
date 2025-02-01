import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from api.tmdb_currently_showing import movies_blueprint
from api.tmdb_popularity_showing import popularity_blueprint
from api.tmdb_rating_showing import rating_blueprint
from api.tmdb_search_showing import search_blueprint

app = Flask(__name__, static_folder='./frontend/build', static_url_path='')
CORS(app)

# Blueprintを登録
app.register_blueprint(movies_blueprint, url_prefix='/api/movies')
app.register_blueprint(popularity_blueprint, url_prefix='/api/popularity')
app.register_blueprint(rating_blueprint, url_prefix='/api/rating')
app.register_blueprint(search_blueprint, url_prefix='/api/search')

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)