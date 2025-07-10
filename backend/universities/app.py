from flask import Flask, jsonify
from config import Config
from flasgger import Swagger
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config.from_object(Config)

swagger = Swagger(app)


@app.route("/health")
def health():
    """
    Health check
    ---
    responses:
      200:
        description: Pong!
    """
    return "Auth service OK"


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return jsonify({
        "error": e.description,
        "code": e.code
    }), e.code


@app.errorhandler(Exception)
def unhandled_exception(error):
    return jsonify({"error": str(error)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)