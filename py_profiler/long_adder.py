import threading

#
# @author andy
#
class LongAdder:
    def __init__(self):
        self._lock = threading.Lock()
        self._value = 0

    def get_value(self):
        return self._value

    def increment(self):
        with self._lock:
            self._value += 1

    def decrement(self):
        with self._lock:
            self._value -= 1

    def set(self, amount: int):
        with self._lock:
            self._value += amount

    def reset(self):
        with self._lock:
            self._value = 0


