from py_profiler import profiler, profiling_service


@profiler('hello')
def hello():
    print('hello')


class Foo:

    @profiler('Food.some_thing')
    def some_thing(self):
        print('some_thing')

    @profiler()
    def method_2(self):
        print('method_2')
        raise Exception('aaaa')


if __name__ == "__main__":
    try:
        foo = Foo()
        hello()
        foo.some_thing()
        foo.method_2()
    except Exception as e:
        pass
    finally:
        print(profiling_service.as_table())
