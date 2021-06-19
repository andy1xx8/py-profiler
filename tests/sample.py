from py_profiler import profiler, profiling_service


@profiler('hello')
def hello():
    print('hello')


if __name__ == "__main__":
    hello()

    print(profiling_service.as_table())