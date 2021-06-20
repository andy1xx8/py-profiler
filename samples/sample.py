from py_profiler import profiler, profiling_service

from src.py_profiler import Profiler


@profiler('hello')
def hello():
    print('hello')


def hello_2():
    with Profiler("hello_2_with_context") as a:
        print('hello_2_with_context')

    print('end hello_2')


class Foo:

    @profiler('Food.some_thing')
    def some_thing(self):
        print('some_thing')

    @profiler
    def method_2(self):
        print('method_2')


if __name__ == "__main__":
    foo = Foo()

    hello()
    hello_2()
    foo.some_thing()
    foo.method_2()

    print(profiling_service.as_table())
