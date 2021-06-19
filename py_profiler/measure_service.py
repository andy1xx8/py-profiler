import threading

from py_profiler.long_adder import LongAdder


#
# @author: anhlt
#
class MeasureValue:
    def __init__(self, func_name: str):
        self._lock = threading.Lock()

        self.func_name = func_name
        self.total_hits = LongAdder()
        self.current_pending_hits = LongAdder()

        self.total_duration_ns = LongAdder()

        # -1: not set
        self.last_duration_ns = -1
        self.lowest_duration_ns = -1
        self.highest_duration_ns = -1

    def start(self):
        self.current_pending_hits.increment()
        self.total_hits.increment()

    def stop(self, duration_ns: int):
        self.current_pending_hits.decrement()
        self.total_duration_ns.set(duration_ns)
        with self._lock:
            self.last_duration_ns = duration_ns
            if self.highest_duration_ns == -1 or self.highest_duration_ns < duration_ns:
                self.highest_duration_ns = duration_ns
            if self.lowest_duration_ns == -1 or self.lowest_duration_ns > duration_ns:
                self.lowest_duration_ns = duration_ns

    def total_duration_as_ms(self):
        return self.total_duration_ns.get_value() / 1000000

    def last_duration_as_ms(self):
        return '{:.3f}'.format(self.last_duration_ns / 1000000)

    def highest_duration_as_ms(self):
        return '{:.3f}'.format(self.highest_duration_ns / 1000000)

    def lowest_duration_as_ms(self):
        return '{:.3f}'.format(self.lowest_duration_ns / 1000000)

    def get_request_rate(self):
        total = self.total_duration_as_ms()
        if total > 0:
            return '{:.3f}'.format(self.total_hits.get_value() * 1000 / total)
        else:
            return ""

    def get_avg_time_per_request(self):
        if self.total_hits.get_value() > 0:
            return '{:.3f}'.format(self.total_duration_as_ms() / self.total_hits.get_value())
        else:
            return ""


class MeasureService:

    @classmethod
    def get_measure_value(self, func_name: str) -> MeasureValue:
        pass

    @classmethod
    def start_measure(self, func_name: str) -> None:
        pass

    @classmethod
    def stop_measure(self, func_name: str, duration_ns: int) -> None:
        pass

    @classmethod
    def get_reports(self) -> list:
        pass

    def get_report_as_html(self) -> str:
        pass

    def as_table(self):
        pass


def _load_template():
    import pkgutil
    data = pkgutil.get_data(__name__, "templates/profiler.html").decode("utf-8")
    from jinja2 import Template
    return Template(data)


class AccumulativeMeasureService(MeasureService):

    def __init__(self):
        self._lock = threading.Lock()
        self._measure_map = dict()
        self._template = _load_template()
        print(f'AccumulativeMeasureService called {__name__}')

    def get_measure_value(self, func_name: str) -> MeasureValue:
        with self._lock:
            if func_name not in self._measure_map:
                self._measure_map[func_name] = MeasureValue(func_name)
        return self._measure_map.get(func_name)

    def start_measure(self, func_name: str) -> None:
        self.get_measure_value(func_name).start()

    def stop_measure(self, func_name: str, duration_ns: int) -> None:
        self.get_measure_value(func_name).stop(duration_ns)

    def get_reports(self) -> list:
        def get_sortable_key(measure_value: MeasureValue):
            return measure_value.func_name

        values = list(self._measure_map.values())
        values.sort(key=get_sortable_key)
        return values

    def get_report_as_html(self) -> str:
        reports = self.get_reports()
        return self._template.render(reports=reports)

    def as_table(self):
        return ''


profiling_service = AccumulativeMeasureService()
