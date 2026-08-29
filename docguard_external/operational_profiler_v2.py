from __future__ import annotations

import statistics
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Iterator


@dataclass
class ThreadSafeLatencyProfiler:
    samples: dict[str, list[float]] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    @contextmanager
    def stage(self, name: str) -> Iterator[None]:
        start = time.perf_counter()
        try:
            yield
        finally:
            self.record(name, time.perf_counter() - start)

    def record(self, name: str, seconds: float) -> None:
        with self._lock:
            self.samples.setdefault(name, []).append(float(seconds))

    def summary(self) -> dict[str, Any]:
        with self._lock:
            snapshot = {key: list(values) for key, values in self.samples.items()}
        report: dict[str, Any] = {}
        for key, values in sorted(snapshot.items()):
            if not values:
                continue
            ordered = sorted(values)
            p95_index = min(len(ordered) - 1, int(len(ordered) * 0.95))
            report[key] = {
                "count": len(values),
                "total_seconds": round(sum(values), 6),
                "mean_seconds": round(sum(values) / len(values), 6),
                "p50_seconds": round(statistics.median(values), 6),
                "p95_seconds": round(ordered[p95_index], 6),
            }
        return report
