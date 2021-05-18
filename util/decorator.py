import time
import functools
from datetime import datetime


def timer(func):
	@functools.wraps(func)
	def wrapper_timer(*args, **kwargs):
		start_time = time.perf_counter()
		value = func(*args, **kwargs)
		end_time = time.perf_counter()
		run_time = end_time -start_time
		print(datetime.utcnow(), f'Finished {func.__name__!r} in {run_time:.4f} secs')
		return value
	return wrapper_timer
