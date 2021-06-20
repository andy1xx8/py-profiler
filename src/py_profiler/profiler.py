import time

from .measure_service import profiling_service


class Profiler(object):
    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        self.begin_time = time.time_ns()
        profiling_service.start_measure(self.name)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type)
        print(exc_val)
        print(exc_tb)
        profiling_service.stop_measure(
            self.name,
            time.time_ns() - self.begin_time
        )
