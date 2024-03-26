from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from auth.auth import requires_auth
from database.models import Actor, Movie, setup_db


def create_app(active=True, test_config=None):
    app = Flask(__name__)
    with app.app_context():
        if active:
            setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PUT, PATCH, DELETE')
        return response

# --------------------------------------------------------------
# Movie
# --------------------------------------------------------------

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def movies(payload):
        try:
            movies = Movie.query.all()
            movie_data = []
            for movie in movies:
                movie_data.append({
                    'id': movie.id,
                    'title': movie.title,
                    'release_date': movie.release_date.strftime('%Y-%m-%d')
                })
            response = {
                'success': True,
                'Movies': movie_data
            }
            return jsonify(response), 200

        except Exception as e:
            abort(401)

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def movies_detail(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)

            if not movie:
                abort(404)

            response = {
                'success': True,
                'id': movie.id,
                'title': movie.title,
                'release_date': movie.release_date.strftime('%Y-%m-%d')
            }
            return jsonify(response), 200

        except Exception as e:
            abort(401)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        try:

            data = request.json
            title = data['title']
            release_date = data['release_date']

            new_movie = Movie(title=title, release_date=release_date)

            Movie.insert(new_movie)

            response = {
                'success': True,
                'message': 'Movie added successfully',
                'movie': new_movie.title
            }
            return jsonify(response), 201

        except Exception as e:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movie(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)

            if not movie:
                abort(404)

            upadted_date = request.json
            title = upadted_date['title']
            release_date = upadted_date['release_date']

            Movie.patch(movie, title, release_date)

            response = {
                'success': True,
                'message': 'Movie updated successfully',
                'movie': movie.title
            }
            return jsonify(response), 201

        except Exception as e:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)

            if not movie:
                abort(404)

            Movie.delete(movie)

            response = {
                'success': True,
                'message': 'Movie deleted successfully',
                'movie': movie.title
            }
            return jsonify(response), 201

        except Exception as e:
            abort(422)

# --------------------------------------------------------------
# Actor
# --------------------------------------------------------------

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def actors(payload):
        try:
            actors = Actor.query.all()
            actor_data = []
            for actor in actors:
                actor_data.append({
                    'id': actor.id,
                    'name': actor.name,
                    'age': actor.age,
                    'gender': actor.gender
                })
            response = {
                'success': True,
                'Actors': actor_data
            }
            return jsonify(response), 200

        except Exception as e:
            abort(401)

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def actor_detail(payload, actor_id):
        try:
            actor = Actor.query.get(actor_id)

            if not actor:
                return jsonify(
                    {'success': False, 'error': 'Actor Not Found'}), 404

            response = {
                'success': True,
                'id': actor.id,
                'name': actor.name,
                'age': actor.age,
                'gender': actor.gender
            }
            return jsonify(response), 200

        except Exception as e:
            abort(401)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        try:
            data = request.json
            name = data['name']
            age = data['age']
            gender = data['gender']

            new_actor = Actor(name=name, age=age, gender=gender)

            Actor.insert(new_actor)

            response = {
                'success': True,
                'message': 'actor added successfully',
                'actor': new_actor.name
            }
            return jsonify(response), 201

        except Exception as e:
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actor(payload, actor_id):
        try:
            actor = Actor.query.get(actor_id)

            if not actor:
                abort(404)

            update_data = request.json
            name = update_data['name']
            age = update_data['age']
            gender = update_data['gender']

            Actor.patch(actor, name, age, gender)

            response = {
                'success': True,
                'message': 'actor updated successfully',
                'actor': actor.name
            }
            return jsonify(response), 201

        except Exception as e:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        try:
            actor = Actor.query.get(actor_id)

            if not actor:
                abort(404)

            Actor.delete(actor)

            response = {
                'success': True,
                'message': 'Actor deleted successfully',
                'actor': actor.name
            }
            return jsonify(response), 201

        except Exception as e:
            abort(422)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
