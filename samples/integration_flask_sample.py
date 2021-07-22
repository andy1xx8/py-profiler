from flask import Flask, Blueprint, Request
from waitress import serve

from py_profiler.profiler_controller import profiler_blueprint

router = Blueprint("haha", __name__)

if __name__ == "__main__":
    app = Flask(__name__)

    blueprints = [
        profiler_blueprint,
        router
    ]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    serve(
        app, host="0.0.0.0",
        port=8080
    )
