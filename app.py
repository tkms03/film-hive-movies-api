from flask import Flask
from flask_cors import CORS
from api.tmdb_currently_showing import movies_blueprint
from api.tmdb_popularity_showing import popularity_blueprint
from api.tmdb_rating_showing import rating_blueprint
from api.tmdb_search_showing import search_blueprint

app = Flask(__name__)
CORS(app)

# Blueprintを登録
app.register_blueprint(movies_blueprint, url_prefix='/api/movies')
app.register_blueprint(popularity_blueprint, url_prefix='/api/popularity')
app.register_blueprint(rating_blueprint, url_prefix='/api/rating')
app.register_blueprint(search_blueprint, url_prefix='/api/search')

if __name__ == '__main__':
    app.run(debug=True)