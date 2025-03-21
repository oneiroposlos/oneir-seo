import time
from contextlib import contextmanager
import logging
from typing import Any, Generator

logger = logging.getLogger('timer')


@contextmanager
def latency(description: str) -> Generator[None, Any, None]:
    start_time = time.perf_counter()
    try:
        yield
    finally:
        elapsed_time = (time.perf_counter() - start_time) * 1000  # Convert to milliseconds
        logger.info(f"{description}: {elapsed_time:.3f}ms")
