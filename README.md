# PY Profiler

A library to measure your method, function execution time.

## Usage

It comes with a really easy api to use, you can add `profiler(name = None)` decorator to any method or function you want
to measure its execution time.

E.g:

```python
from py_profiler import profiler


@profiler('hello_execution_measurement')
def hello():
    print('hello')
```

## Access Profiler

1. View as a table

```python
from py_profiler.measure_service import profiling_service

print(profiling_service.as_table())
```

| No | Name                           | Total  | Pending  | Total Exec | Last Exec  | Highest Ex | Request Ra | Avg Time/R |
|    |                                |  Req   |   Req    |    Time    |    Time    |  ec Time   | te (req/se | equest (mi |
|    |                                |        |          |            |            |            |     c)     | llis/reque |
|    |                                |        |          |            |            |            |            |    st)     |
|----|--------------------------------|--------|----------|------------|------------|------------|------------|------------|
| 1  | hello                          |   4    |    0     |   0.046    |   0.005    |   0.029    | 86956.522  |   0.011    |


2. Intergrate with Flask

- If you are using Flask to implement your Restful API. You can add `profiler_blueprint` to your Flash app.

E.g:

```python
from flask import Flask
from waitress import serve
from py_profiler import profiler_blueprint

app = Flask(__name__)
app.register_blueprint(profiler_blueprint)

serve(
    app, 
    host="0.0.0.0",
    port=8080
)
```

Then you can access the profiler page at: `http://127.0.0.1:8080/profiler`
![Py Profiler Page](sample.png)