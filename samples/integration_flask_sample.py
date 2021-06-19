from flask import Flask
from waitress import serve

from py_profiler import profiler_blueprint

if __name__ == "__main__":
    app = Flask(__name__)

    blueprints = [
        profiler_blueprint,
    ]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    serve(
        app, host="0.0.0.0",
        port=8080
    )
