import time

from .measure_service import profiling_service


#
# @author andy
#
def profiler(name=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if name is None:
                try:
                    function_name = func.__func__.__qualname__
                except:
                    function_name = func.__qualname__
            else:
                function_name = name

            # begin_time = time.time_ns()
            is_error = False
            begin_time = time.time() * 1000_000_000
            profiling_service.start_measure(function_name)
            try:
                return func(*args, **kwargs)
            except Exception as error:
                is_error = True
                raise error
            finally:
                profiling_service.stop_measure(
                    function_name,
                    time.time() * 1000_000_000 - begin_time,
                    is_error=is_error
                )

        return wrapper

    return decorator
