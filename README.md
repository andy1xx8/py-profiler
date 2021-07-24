# PY Profiler

A library to measure method, function or your restful api execution time.

## Install

- Run `pip install py-profiler` or `pip3 install py-profiler` to install this library

## Usage

It comes with a really easy api to use, you can add `profiler(name = None)` decorator to any method or function you want
to measure its execution time.

E.g:

```python
from py_profiler import profiler, profiling_service


@profiler('hello')
def hello():
    print('hello')


class Foo:

    @profiler('Food.some_thing')
    def some_thing(self):
        print('some_thing')

    # By default, profiler name is f'{class_name}.{method_name}'
    @profiler()
    def method_2(self):
        print('method_2')

```

## Access Profiler

- Exec time is in milliseconds

1. **View as a table**

```python
from py_profiler import profiling_service

print(profiling_service.as_table())
```

| No | Name                           | Total Req  | Pending Req  | Total Exec Time | Last Exec Time  | Highest Exec Time | Request Rate (req/sec) | Avg Time/Request (millis/req) |
|----|--------------------------------|--------|----------|------------|------------|------------|------------|------------|
| 1  | Foo.method_2                   |   1    |    0     |   0.014    |   0.014    |   0.014    | 71428.571  |   0.014    |
| 2  | Food.some_thing                |   1    |    0     |   0.011    |   0.011    |   0.011    | 90909.091  |   0.011    |
| 3  | hello                          |   1    |    0     |   0.031    |   0.031    |   0.031    | 32258.065  |   0.031    |

2. **Integrate with Flask**

- If you are using Flask to implement your Restful API. You can add `profiler_blueprint` to your Flash app.

E.g:

```python
from flask import Flask
from waitress import serve
from py_profiler.profiler_controller import profiler_blueprint

app = Flask(__name__)
app.register_blueprint(profiler_blueprint)

serve(
    app,
    host="0.0.0.0",
    port=8080
)
```

Then you can access the profiler page at: `http://127.0.0.1:8080/profiler`
![Py Profiler Page](https://github.com/andy1xx8/py-profiler/blob/master/sample.png?raw=true)

3. **Integrate with 3rd restful library**.

You can build your custom profiler viewer by using `as_html()`

```python
from py_profiler import profiling_service

html_page = profiling_service.as_html()
```

Then, you can implement a html page and return this `html_page` to your client to see profiler viewer.