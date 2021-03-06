import datetime
import threading
import time

from beautifultable import BeautifulTable

from . import utils
from .long_adder import LongAdder
#
# @author: andy
#
from .utils import load_jinja2_template


class MeasureValue:
    def __init__(self, func_name: str):
        self._lock = threading.Lock()

        self.func_name = func_name
        self.total_hits = LongAdder()
        self.current_error_hits = LongAdder()
        self.current_pending_hits = LongAdder()

        self.total_duration_ns = LongAdder()

        # -1: not set
        self.last_duration_ns = -1
        self.lowest_duration_ns = -1
        self.highest_duration_ns = -1

    def start(self):
        self.current_pending_hits.increment()
        self.total_hits.increment()

    def stop(self, duration_ns: int, is_error: bool = False):
        if is_error:
            self.current_error_hits.increment()

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

    def get_measure_value(self, func_name: str) -> MeasureValue:
        pass

    def start_measure(self, func_name: str) -> None:
        pass

    def stop_measure(self, func_name: str, duration_ns: int, is_error: bool = False) -> None:
        pass

    def get_uptime(self) -> int:
        pass

    def get_reports(self) -> list:
        pass

    def as_html(self) -> str:
        pass

    def as_table(self) -> str:
        pass


class AccumulativeMeasureService(MeasureService):

    def __init__(self):
        self._lock = threading.Lock()
        self._measure_map = dict()
        self._template = load_jinja2_template("templates/profiler.html")
        self.start_at = time.time() * 1000
        print(f'AccumulativeMeasureService called {__name__}')

    def get_measure_value(self, func_name: str) -> MeasureValue:
        with self._lock:
            if func_name not in self._measure_map:
                self._measure_map[func_name] = MeasureValue(func_name)
        return self._measure_map.get(func_name)

    def start_measure(self, func_name: str) -> None:
        self.get_measure_value(func_name).start()

    def stop_measure(self, func_name: str, duration_ns: int, is_error: bool = False) -> None:
        self.get_measure_value(func_name).stop(duration_ns, is_error)

    def get_uptime(self) -> int:
        return int(time.time() * 1000) - int(self.start_at)

    def get_reports(self) -> list:
        def get_sortable_key(measure_value: MeasureValue):
            return measure_value.func_name

        values = list(self._measure_map.values())
        values.sort(key=get_sortable_key)
        return values

    def as_html(self) -> str:
        reports = self.get_reports()
        uptime_str = utils.pretty_time_delta(int(self.get_uptime() / 1000))
        start_at_str = datetime.datetime.fromtimestamp(int(self.start_at / 1000)).strftime("%Y-%m-%d %H:%M:%S")
        return self._template.render(
            reports=reports,
            uptime=uptime_str,
            start_at=start_at_str
        )

    def as_table(self):
        table = BeautifulTable()
        table.columns.header = [
            "No",
            "Name",
            "Total Req",
            "Pending Req",
            "Error Req",
            "Total Exec Time",
            "Last Exec Time",
            "Highest Exec Time",
            "Request Rate (req/sec)",
            "Avg Time/Request (millis/request)",
        ]
        table.columns.alignment['Name'] = BeautifulTable.ALIGN_LEFT

        table.columns.width = 12
        table.columns.width["No"] = 4
        table.columns.width["Total Req"] = 8
        table.columns.width["Pending Req"] = 10
        table.columns.width["Name"] = 32

        for i, report in enumerate(self.get_reports()):
            table.rows.append([
                i + 1,
                report.func_name,
                report.total_hits.get_value(),
                report.current_pending_hits.get_value(),
                report.current_error_hits.get_value(),
                report.total_duration_as_ms(),
                report.last_duration_as_ms(),
                report.highest_duration_as_ms(),
                report.get_request_rate(),
                report.get_avg_time_per_request()
            ])
        return str(table)

# Create
profiling_service = AccumulativeMeasureService()
