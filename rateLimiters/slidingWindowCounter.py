import time
from collections import defaultdict
from typing import DefaultDict, Dict


class SlidingWindowCounter:
    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size
        self.max_requests = max_requests

        self.request_counts: DefaultDict[str, Dict[str, float | int]] = defaultdict(
            lambda: {
                "current_window_start": 0,
                "current_count": 0,
                "previous_count": 0,
            }
        )

    def is_allowed(self, ip_address: str) -> bool:
        current_time = time.time()

        current_window_start = current_time - (current_time % self.window_size)

        client_data = self.request_counts[ip_address]

        # First request for this IP
        if client_data["current_window_start"] == 0:
            client_data["current_window_start"] = current_window_start

        # If we moved into a new window
        if current_window_start > client_data["current_window_start"]:
            windows_passed = (
                current_window_start - client_data["current_window_start"]
            ) / self.window_size

            if windows_passed == 1:
                client_data["previous_count"] = client_data["current_count"]
            else:
                client_data["previous_count"] = 0

            client_data["current_count"] = 0
            client_data["current_window_start"] = current_window_start

        time_into_current_window = current_time - client_data["current_window_start"]
        time_remaining = self.window_size - time_into_current_window

        previous_window_weight = time_remaining / self.window_size

        estimated_count = (
            client_data["previous_count"] * previous_window_weight
            + client_data["current_count"]
        )

        if estimated_count < self.max_requests:
            client_data["current_count"] += 1
            return True

        return False
