from flask import Flask
from waitress import serve

from py_profiler import profiler, profiling_service
from py_profiler import profiler_blueprint


@profiler('hello')
def hello():
    print('hello')


def setup_blueprints(
        port: int = 8080,
        nthreads: int = 2,
) -> None:
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.debug = True

    blueprints = [
        profiler_blueprint,
    ]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    print(f"Created http server at port = {port} with {nthreads} concurrent threads.")
    serve(
        app, host="0.0.0.0",
        port=port,
        threads=nthreads if nthreads is not None else 4
    )


if __name__ == "__main__":
    hello()
    hello()
    hello()
    hello()
    print(profiling_service.as_table())
    setup_blueprints()
