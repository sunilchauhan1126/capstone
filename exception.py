
from flask import jsonify
import api as app
from auth.auth import AuthError


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404


@app.errorhandler(401)
def not_found_error(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "UnAuthorised"
    }), 404


@app.errorhandler(AuthError)
def handle_auth_error(e):
    response = jsonify(e.error)
    response.status_code = e.status_code
    return response
